(function () {
  'use strict';

  var app = angular.module('app');

  app.controller('emrCtrl', function($scope) {

    $scope.dialog = {
      visible: false
    };

    $scope.dialog = function(title, text, callback, cancelCallback) {
      $scope.dialog.title = title;
      $scope.dialog.text = text;
      $scope.dialog.callback = callback;
      $scope.dialog.visible = true;
      $scope.dialog.ok = function() {
        $scope.dialog.visible = false;
        if(callback) callback();
      };
      $scope.dialog.cancel = function() {
        $scope.dialog.visible = false;
        if(cancelCallback) cancelCallback();
      };
    };

    $scope.format_number = function(value, digits_after_comma=2) {
      return parseFloat('' + value).toFixed(digits_after_comma);
    };

    $scope.format_percent = function(value) {
      return $scope.format_number(parseFloat('' + value) * 100.0) + " %"
    };

    $scope.format_datetime = function(ms) {
      var a = new Date(parseInt(ms));
      //var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
      //var month = months[a.getMonth()];
      var month = a.getMonth() + 1;
      month = month < 10 ? '0' + month : month;
      var year = a.getFullYear();
      var date = a.getDate() < 10 ? '0' + a.getDate() : a.getDate();
      var hour = a.getHours() < 10 ? '0' + a.getHours() : a.getHours();
      var min = a.getMinutes() < 10 ? '0' + a.getMinutes() : a.getMinutes();
      var sec = a.getSeconds() < 10 ? '0' + a.getSeconds() : a.getSeconds();
      var time = year + '-' + month + '-' + date + ' ' + hour + ':' + min + ':' + sec ;
      return time;
    };

    $scope.format_duration = function(seconds) {
      var interval = Math.floor(seconds / 31536000);
      if (interval > 1) {
          return interval + " years";
      }
      interval = Math.floor(seconds / 2592000);
      if (interval > 1) {
          return interval + " months";
      }
      interval = Math.floor(seconds / 86400);
      if (interval > 1) {
          return interval + " days";
      }
      interval = Math.floor(seconds / 3600);
      if (interval > 1) {
          return interval + " hours";
      }
      interval = Math.floor(seconds / 60);
      if (interval > 1) {
          return interval + " minutes";
      }
      return Math.floor(seconds) + " seconds";
    };

    $scope.format_currency = function(amount, currency='USD', digits_after_comma=2) {
      return currency + ' ' + $scope.format_number(amount, digits_after_comma);
    };

    $scope.arrayRemove = function(array, el) {
      for(var i = array.length - 1; i >= 0; i--) {
        if(array[i] === el) {
           array.splice(i, 1);
        }
      }
    }
  });

})();