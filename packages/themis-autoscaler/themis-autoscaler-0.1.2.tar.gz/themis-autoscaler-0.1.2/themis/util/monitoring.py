import subprocess
import re
import os
import json
import math
import time
import sqlite3
import themis
from datetime import timedelta, datetime
from scipy import integrate
from themis import constants
from themis.util import aws_common, common, expr
from themis.util.common import *
from themis.util.remote import run_ssh

# logger
LOG = get_logger(__name__)

# global DB connection
db_connection = None
DB_FILE_NAME = 'monitoring.data.db'

# get data from the last 10 minutes
MONITORING_INTERVAL_SECS = 60 * 10

# default minimum task nodes
DEFAULT_MIN_TASK_NODES = 1


def remove_nan(array):
    i = 0
    while i < len(array):
        for item in array[i]:
            if item == 'NaN' or math.isnan(item):
                del array[i]
                i -= 1
                break
        i += 1
    return array


def get_time_duration(datapoints):
    start = float('inf')
    end = 0
    for d in datapoints:
        if d[1] > end:
            end = d[1]
        if d[1] < start:
            start = d[1]
    return end - start


def get_node_load_part(cluster_ip, cluster_id, host, type, monitoring_interval_secs=MONITORING_INTERVAL_SECS):
    diff_secs = monitoring_interval_secs
    format = "%m/%d/%Y %H:%M"
    start_time, end_time = get_start_and_end(diff_secs, format)
    type_param = 'mem_report' if type == 'mem' else 'cpu_report' if type == 'cpu' else 'invalid'
    url = 'http://%s/ganglia/graph.php?h=%s&cs=%s&ce=%s&c=%s&g=%s&json=1' % (
        cluster_ip, host, start_time, end_time, cluster_id, type_param)
    cmd = "curl --connect-timeout %s '%s' 2> /dev/null" % (CURL_CONNECT_TIMEOUT, url)
    result = run(cmd, GANGLIA_CACHE_TIMEOUT)
    result = json.loads(result)
    mem_total = 0.0
    mem_free = 0.0
    if not result:
        return float('NaN')
    for curve in result:
        datapoints = curve['datapoints']
        if curve['ds_name'] == 'bmem_total':
            remove_nan(datapoints)
            rev_curve = array_reverse(datapoints)
            if len(rev_curve) >= 2:
                mem_total = integrate.simps(rev_curve[0], rev_curve[1])
        if curve['ds_name'] == 'bmem_free':
            remove_nan(datapoints)
            rev_curve = array_reverse(datapoints)
            if len(rev_curve) >= 2:
                mem_free = integrate.simps(rev_curve[0], rev_curve[1])
        if curve['ds_name'] == 'cpu_idle':
            remove_nan(datapoints)
            rev_curve = array_reverse(datapoints)
            integrated = 0
            if len(rev_curve) >= 2:
                integrated = integrate.simps(rev_curve[0], rev_curve[1])
            time_duration = get_time_duration(datapoints)
            total = time_duration * 100.0
            percent = 1.0 - (integrated / total)
            if type == 'cpu':
                return percent
    if type == 'mem':
        if mem_total == 0:
            return float('NaN')
        return 1.0 - (mem_free / mem_total)
    return float('NaN')


def get_node_load_cpu(cluster_ip, cluster_id, host, monitoring_interval_secs=MONITORING_INTERVAL_SECS):
    return get_node_load_part(cluster_ip, cluster_id, host, 'cpu', monitoring_interval_secs)


def get_node_load_mem(cluster_ip, cluster_id, host, monitoring_interval_secs=MONITORING_INTERVAL_SECS):
    return get_node_load_part(cluster_ip, cluster_id, host, 'mem', monitoring_interval_secs)


def get_node_load(cluster_ip, cluster_id, host, monitoring_interval_secs=MONITORING_INTERVAL_SECS):
    result = {}
    result['mem'] = get_node_load_mem(cluster_ip, cluster_id, host, monitoring_interval_secs)
    result['cpu'] = get_node_load_cpu(cluster_ip, cluster_id, host, monitoring_interval_secs)
    return result


def get_cluster_load(cluster_info, nodes=None, monitoring_interval_secs=MONITORING_INTERVAL_SECS):
    cluster_id = cluster_info['id']
    cluster_ip = cluster_info['ip']
    result = {}
    if not nodes:
        nodes = aws_common.get_cluster_nodes(cluster_id)

    def query(node):
        cluster_ip = cluster_info['ip']
        host = node['host']
        try:
            load = get_node_load(cluster_ip, cluster_id, host, monitoring_interval_secs)
            result[host] = load
        except Exception, e:
            try:
                # Ganglia is only available via public IP address
                # (necessary if running the autoscaling webserver outside AWS)
                cluster_ip = cluster_info['ip_public']
                load = get_node_load(cluster_ip, cluster_id, host, monitoring_interval_secs)
                result[host] = load
            except Exception, e:
                LOG.warning("Unable to get load for node %s: %s" % (host, e))
                result[host] = {}

    parallelize(nodes, query)
    return result


def get_presto_node_states(nodes, cluster_ip):
    def query(host, node_info):
        node_info['presto_state'] = 'N/A'
        try:
            if node_info['state'] == aws_common.INSTANCE_STATE_RUNNING:
                state = aws_common.get_presto_node_state(cluster_ip, host)
                node_info['presto_state'] = state
        except Exception, e:
            if host[0:9] == 'testhost-':
                # for testing purposes
                node_info['presto_state'] = aws_common.PRESTO_STATE_ACTIVE
            # swallow this exception. It occurs if the node has been shutdown (i.e., JVM
            # process on node is terminated) but the instance has not been terminated yet
            pass

    parallelize(nodes, query)


def get_node_queries(cluster_ip):
    cmd = ('presto-cli --execute \\"SELECT n.http_uri,count(q.node_id) from system.runtime.nodes n ' +
        'left join (select * from system.runtime.queries where state = \'RUNNING\' ) as q ' +
        'on q.node_id = n.node_id group by n.http_uri\\"')

    result = {}
    if cluster_ip == 'localhost':
        # for testing purposes
        return result

    # run ssh command
    out = run_ssh(cmd, cluster_ip, user='hadoop', cache_duration_secs=QUERY_CACHE_TIMEOUT)

    # remove SSH log output line
    out = remove_lines_from_string(out, r'.*Permanently added.*')

    # read config for domain
    custom_dn = config.get_value(constants.KEY_CUSTOM_DOMAIN_NAME, section=cluster_id)
    # assume input is actually domain name (not ip)
    dn = custom_dn if custom_dn else re.match(r'ip-[^\.]+\.(.+)', cluster_ip).group(1)

    for line in out.splitlines():
        ip = re.sub(r'.*http://([0-9\.]+):.*', r'\1', line)
        if ip:
            queries = re.sub(r'.*"([0-9\.]+)"$', r'\1', line)
            host = aws_common.ip_to_hostname(ip, dn)
            try:
                result[host] = int(queries)
            except Exception, e:
                result[host] = 0
    return result


def get_idle_task_nodes(queries):
    result = []
    for host in queries:
        if queries[host] == "0":
            result.append(host)
    return result


def do_add_stats(nodelist, result_map):
    result_map['average'] = {}
    result_map['sum'] = {}
    result_map['count'] = {}
    result_map['running'] = True
    result_map['active'] = True
    sum_cpu = 0.0
    sum_mem = 0.0
    sum_queries = 0.0
    for item in nodelist:
        if 'load' in item:
            if 'mem' in item['load'] and is_float(item['load']['mem']):
                sum_mem += item['load']['mem']
            if 'cpu' in item['load'] and is_float(item['load']['cpu']):
                sum_cpu += item['load']['cpu']
        if 'queries' in item:
            sum_queries += item['queries']
        if 'state' not in item:
            item['state'] = 'N/A'
        if item['state'] != aws_common.INSTANCE_STATE_RUNNING:
            result_map['running'] = False
        if 'presto_state' not in item:
            item['presto_state'] = 'N/A'
        if item['presto_state'] != aws_common.PRESTO_STATE_ACTIVE:
            result_map['active'] = False
    result_map['average']['cpu'] = 'NaN'
    result_map['average']['mem'] = 'NaN'
    result_map['average']['queries'] = 'NaN'
    if len(nodelist) > 0:
        result_map['average']['cpu'] = sum_cpu / len(nodelist)
        result_map['average']['mem'] = sum_mem / len(nodelist)
        result_map['average']['queries'] = sum_queries / len(nodelist)
    result_map['sum']['queries'] = sum_queries
    result_map['count']['nodes'] = len(nodelist)


def add_stats(data):
    if 'nodes_list' in data:
        data['allnodes'] = {}
        do_add_stats(data['nodes_list'], data['allnodes'])

        data['tasknodes'] = {}
        data['corenodes'] = {}
        data['masternodes'] = {}
        task_nodes = [n for n in data['nodes_list'] if n['type'] == aws_common.INSTANCE_GROUP_TYPE_TASK]
        do_add_stats(task_nodes, data['tasknodes'])
        master_nodes = [n for n in data['nodes_list'] if n['type'] == aws_common.INSTANCE_GROUP_TYPE_MASTER]
        do_add_stats(master_nodes, data['masternodes'])
        core_nodes = [n for n in data['nodes_list'] if n['type'] == aws_common.INSTANCE_GROUP_TYPE_CORE]
        do_add_stats(core_nodes, data['corenodes'])


def collect_info(cluster_info, nodes=None, config=None,
        monitoring_interval_secs=MONITORING_INTERVAL_SECS):
    cluster_id = cluster_info['id']
    cluster_ip = cluster_info['ip']
    result = {}
    result['time_based'] = {}
    time_based_config = get_time_based_scaling_config(cluster_id, config=config)
    result['time_based']['enabled'] = len(time_based_config) > 0
    result['time_based']['minimum'] = {}
    result['nodes'] = {}
    result['cluster_id'] = cluster_id
    result['is_presto'] = cluster_info['type'] == aws_common.CLUSTER_TYPE_PRESTO
    nodes_list = nodes
    if not nodes_list:
        nodes_list = aws_common.get_cluster_nodes(cluster_id)
    for node in nodes_list:
        host = node['host']
        result['nodes'][host] = {}
        result['nodes'][host]['type'] = node['type']
        result['nodes'][host]['state'] = node['state']
        result['nodes'][host]['cid'] = node['cid']
        result['nodes'][host]['iid'] = node['iid']
        result['nodes'][host]['gid'] = node['gid']
        result['nodes'][host]['queries'] = 0
        result['nodes'][host]['market'] = node['market']
    try:
        queries = get_node_queries(cluster_ip)
        for host in queries:
            if host not in result['nodes']:
                result['nodes'][host] = {}
            result['nodes'][host]['queries'] = queries[host]
        result['idle_nodes'] = get_idle_task_nodes(queries)
    except subprocess.CalledProcessError, e:
        # happens for non-presto clusters (where presto-cli is not available)
        pass
    result['nodes_list'] = []
    for host in result['nodes']:
        entry = result['nodes'][host]
        entry['host'] = host
        result['nodes_list'].append(entry)
    node_infos = get_cluster_load(cluster_info, nodes=nodes,
        monitoring_interval_secs=monitoring_interval_secs)
    for host in node_infos:
        result['nodes'][host]['load'] = node_infos[host]
        if 'presto_state' in result['nodes'][host]:
            result['nodes'][host]['presto_state'] = node_infos[host]
    if result['is_presto']:
        get_presto_node_states(result['nodes'], cluster_ip)

    add_stats(result)
    remove_NaN(result)
    return result


def history_get_db():
    local = threading.local()
    db_connection = None
    try:
        db_connection = local.db_connection
    except AttributeError:
        pass
    if not db_connection:
        db_connection = sqlite3.connect(DB_FILE_NAME)
        local.db_connection = db_connection
        c = db_connection.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS states ' +
            '(timestamp text unique, cluster text, state text, action text)')
        db_connection.commit()
    return db_connection


def execute_dsl_string(str, context, config=None):
    expr_context = expr.ExprContext(context)
    allnodes = expr_context.allnodes
    tasknodes = expr_context.tasknodes
    time_based = expr_context.time_based
    cluster_id = context['cluster_id']

    def get_min_nodes_for_cluster(date):
        return get_minimum_nodes(date, cluster_id)
    time_based.minimum.nodes = get_min_nodes_for_cluster
    now = datetime.utcnow()
    now_override = themis.config.get_value(constants.KEY_NOW, config=config, default=None)
    if now_override:
        now = now_override
    return eval(str)


def history_add(cluster, state, action):
    nodes = state['nodes']
    state['nodes'] = {}
    del state['nodes_list']
    state['groups'] = {}
    for key, val in nodes.iteritems():
        instance_id = val['iid']
        group_id = val['gid']
        if group_id not in state['groups']:
            state['groups'][group_id] = {'instances': []}
        state['groups'][group_id]['instances'].append({
            'iid': val['iid']
            # TODO add more relevant data to persist
        })
    state = json.dumps(state)
    conn = history_get_db()
    c = conn.cursor()
    ms = time.time() * 1000.0
    c.execute("INSERT INTO states(timestamp,cluster,state,action) " +
        "VALUES (?,?,?,?)", (ms, cluster, state, action))
    conn.commit()


def history_get(cluster, limit=100):
    conn = history_get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM states WHERE cluster=? " +
        "ORDER BY timestamp DESC LIMIT ?", (cluster, limit))
    result = [dict((c.description[i][0], value)
                   for i, value in enumerate(row)) for row in c.fetchall()]
    for entry in result:
        if 'state' in entry:
            entry['state'] = json.loads(entry['state'])
    return result


def get_time_based_scaling_config(cluster_id, config=None):
    result = themis.config.get_value(constants.KEY_TIME_BASED_SCALING,
        config=config, default='{}', section=cluster_id)
    try:
        return json.loads(result)
    except Exception, e:
        return {}


# returns nodes if based on regex dict values
# assumes no overlapping entries as will grab the first item it matches.
def get_minimum_nodes(date, cluster_id):
    now_str = date.strftime("%a %Y-%m-%d %H:%M:%S")

    # This is only used for testing, to overwrite the config. If TEST_CONFIG is
    # None (which is the default), then the actual configuration will be used.
    config = themis.config.TEST_CONFIG

    pattern_to_nodes = get_time_based_scaling_config(cluster_id=cluster_id, config=config)
    nodes_to_return = None
    for pattern, num_nodes in pattern_to_nodes.iteritems():
        if re.match(pattern, now_str):
            if nodes_to_return is None:
                nodes_to_return = num_nodes
            else:
                LOG.warning(("'%s' Regex Pattern has matched more than once:\nnodes_to_return=%d " +
                    "is now changing to nodes_to_return=%d") % (pattern, nodes_to_return, num_nodes))
                nodes_to_return = num_nodes
    # no match revert to default
    if nodes_to_return is None:
        return DEFAULT_MIN_TASK_NODES
    return nodes_to_return
