var hidashApp = angular.module('dashboard', ['googlechart','hidash', 'ui.bootstrap']);
hidashApp.config(function($locationProvider) {
    $locationProvider.html5Mode({
      enabled: true,
      requireBase: false
    });
});
hidashApp.controller('ReportsController',function($scope, $http, $window, $location){
  $scope.filters = [];
  $scope.renderFlag = false;
  $scope.group = '';
  if('group' in $location.search()) {
    $scope.group = $location.search()['group'];
    $http.get('/hidash-api/get_group_filters.json/?group=' + $scope.group).success(function(filters) {
      $scope.filters = filters;
      $scope.paramsList = [];
      $scope.parameters = [];
      $scope.filterLabels = [];
      for (var i = 0; i < $scope.filters.length; i++) {
        if($scope.filters[i].type === 'datetime') {
          $scope.filterLabels.push($scope.filters[i].name.replace(/_/g, " "));
          var date = new Date();
          date.setDate(1);
          if($scope.filters[i].filter_value !== null){
            date = $scope.filters[i].filter_value;
          }
          date = $location.search()[$scope.filters[i].name] ? $location.search()[$scope.filters[i].name] : date;
          $scope.parameters.push(date);
        }
        else if($scope.filters[i].type === 'daterange') {
          var labels = [$scope.filters[i].name[0].replace(/_/g, " "), $scope.filters[i].name[1].replace(/_/g, " ")];
          $scope.filterLabels.push(labels);
          var start_date = new Date();
          var end_date = new Date();
          start_date.setDate(1);
          end_date.setDate(3);
          if($scope.filters[i].filter_value !== null){
            start_date = $scope.filters[i].filter_value[0];
            end_date = $scope.filters[i].filter_value[1];
          }
          start_date = $location.search()[$scope.filters[i].name[0]] ? $location.search()[$scope.filters[i].name[0]]: start_date;
          end_date = $location.search()[$scope.filters[i].name[1]] ? $location.search()[$scope.filters[i].name[1]]: end_date;
          date = [start_date, end_date];
          $scope.parameters.push(date);
        }
        else {
          $scope.filterLabels.push($scope.filters[i].name.replace(/_/g, " "));
          var dropdownParam = '1';
          dropdownParam = $location.search()[$scope.filters[i].name] ? $location.search()[$scope.filters[i].name] : dropdownParam;
          $scope.parameters.push(dropdownParam);
        }
      }
      $scope.$watch('parameters', function() {
        newParams = '';
        urlParamsObj = {group: $scope.group};
        for (var  i= 0;i<$scope.parameters.length;i++) {
          if($scope.filters[i].type === 'datetime') {
            newParams += $scope.filters[i].name + '=' + moment($scope.parameters[i]).format("YYYY-MM-DD") + ',';
            urlParamsObj[$scope.filters[i].name] = moment($scope.parameters[i]).format("YYYY-MM-DD");
          }
          else if ($scope.filters[i].type === 'daterange'){
            newParams += $scope.filters[i].name[0] +'=' + moment($scope.parameters[i][0]).format("YYYY-MM-DD 00:00:00") +'&'+$scope.filters[i].name[1] +'=' + moment($scope.parameters[i][1]).format("YYYY-MM-DD 23:59:59") + ',';
            urlParamsObj[$scope.filters[i].name[0]] = moment($scope.parameters[i][0]).format("YYYY-MM-DD 00:00:00");
            urlParamsObj[$scope.filters[i].name[1]] = moment($scope.parameters[i][1]).format("YYYY-MM-DD 23:59:59");
          }
          else {
            newParams += $scope.filters[i].name + '=' + $scope.parameters[i] + ', ';
            urlParamsObj[$scope.filters[i].name] = $scope.parameters[i];
          }
        }
        $scope.params = newParams;
        $location.search(urlParamsObj);
      }, true);
      $scope.renderFlag = true;
    });
  }
})
.directive('hiDash', ['$http', function($http) {
  return {
    restrict: 'E',
    template:
    "<div id='dashboard' class='container'>"+
      "<div class='hidash-dashboard-filter row'>"+
        "<div ng-repeat='filter in filters'>"+
          "<div class='date'>"+
            '<div ng-if="filter.type===\'datetime\'">'+
              '<div class="col-md-{{filter.grid_width}} col-xs-{{filter.grid_width}}">'+
              "<label class='filter-labels'>{{filterLabels[$index]}}</label>"+
              "<p class='input-group'>"+
                "<input type='text' class='form-control' datepicker-popup='dd MMM yyyy' date-time-picker-set-local ng-model='parameters[$index]' datepicker-options='dateOptions' name='HidashStartDate' show-weeks='false' close-text='Close' ng-model-onblur/>"+
                "<span class='input-group-btn input-group-hidash-icon'>"+
                  "<i class='fa fa-calendar' aria-hidden='true'></i>"+
                "</span>"+
                "</p>"+
                "</div>"+
              "</div>"+
              '<div ng-if="filter.type===\'dropdown\'">'+
                '<div class="col-md-{{filter.grid_width}} col-xs-{{filter.grid_width}}">'+
                "<label class='filter-labels'>{{filterLabels[$index]}}</label>"+
                '<select ng-model="parameters[$index]" class="form-control">'+
                  "<option ng-repeat='value in filter.filter_values' value={{value.value}}>{{value.name}}</option>"+
                '</select>'+
                '</div>'+
              "</div>"+
              '<div ng-if="filter.type===\'daterange\'">'+
              '<div class="col-md-{{filter.grid_width}} col-xs-{{filter.grid_width}}">'+
              "<label class='filter-labels'>{{filterLabels[$index][0]}}</label>"+
              "<p class='input-group'>"+
                "<input type='text' class='form-control' datepicker-popup='dd MMM yyyy' date-time-picker-set-local ng-model='parameters[$index][0]' datepicker-options='dateOptions' name='HidashStartDateRange' show-weeks='false' close-text='Close' ng-model-onblur/>"+
                "<span class='input-group-btn input-group-hidash-icon'>"+
                  "<i class='fa fa-calendar' aria-hidden='true'></i>"+
                "</span>"+
                "</p>"+
              '</div>'+
              '<div class="col-md-{{filter.grid_width}} col-xs-{{filter.grid_width}}">'+
                "<label class='filter-labels'>{{filterLabels[$index][1]}}</label>"+
                "<p class='input-group'>"+
                "<input type='text' class='form-control' datepicker-popup='dd MMM yyyy' date-time-picker-set-local ng-model='parameters[$index][1]' datepicker-options='dateOptions' name='HidashEndDateRange' show-weeks='false' close-text='Close' ng-model-onblur/>"+
                "<span class='input-group-btn input-group-hidash-icon'>"+
                  "<i class='fa fa-calendar' aria-hidden='true'></i>"+
                "</span>"+
                "</p>"+
              "</div>"+
              "</div>"+
          "</div>"+
        "</div>"+
      "</div>"+
      "<hi-dash-reports group={{group}} params='{{params}}' render-flag='renderFlag'></hi-dash-reports>"+
    "</div>"
  };
}])
.directive('pageOverlayPace', function($window) {
    return {
        restrict: 'E',
        template: '<div class="pace-overlay"></div>',
        link: function (scope, element) {
            //Fixme: Pace issue, start event is not firing on page load.
            //Using this workaround to handle it.
            element.ready(function() {
                $("div.pace-overlay").show();
            });
            Pace.on("start", function(){
                $("div.pace-overlay").show();
            });

            Pace.on("done", function(){
                $("div.pace-overlay").hide();
            });
        }
    }
});
