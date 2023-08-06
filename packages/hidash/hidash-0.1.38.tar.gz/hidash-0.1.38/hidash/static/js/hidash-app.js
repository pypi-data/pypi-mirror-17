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
				$scope.filterLabels.push($scope.filters[i].name.replace(/_/g, " "))
	 			if($scope.filters[i].type === 'datetime') {
	 				var date = new Date();
	 				date.setDate(1);
          date = $location.search()[$scope.filters[i].name] ? $location.search()[$scope.filters[i].name] : date;
	 				if($scope.filters[i].filter_value !== null){
	        	date = $scope.filters[i].filter_value;
	 				}
	        $scope.parameters.push(date);
	 			}
	 			else {
          var dropdownParam = '1';
          dropdownParam = $location.search()[$scope.filters[i].name] ? $location.search()[$scope.filters[i].name] : dropdownParam;
	 				$scope.parameters.push(dropdownParam);
	 			}
	 		}
			$scope.$watch('parameters', function() {
				newParams = '';
        urlParamsObj = {group: $scope.group};
	 			for (var i=0;i<$scope.parameters.length;i++) {
	 				if($scope.filters[i].type === 'datetime') {
            newParams += $scope.filters[i].name + '=' + moment($scope.parameters[i]).format("YYYY-MM-DD") + ',';
            urlParamsObj[$scope.filters[i].name] = moment($scope.parameters[i]).format("YYYY-MM-DD");
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
        	"<div class='date col-md-{{filter.grid_width}} col-xs-{{filter.grid_width}}'>"+
	          "<label class='filter-labels'>{{filterLabels[$index]}}</label>"+
	          '<div ng-if="filter.type===\'datetime\'">'+
	          	"<p class='input-group'>"+
		            "<input type='text' class='form-control' datepicker-popup='dd MMM yyyy' date-time-picker-set-local ng-model='parameters[$index]' datepicker-options='dateOptions' name='HidashStartDate' show-weeks='false' close-text='Close' ng-model-onblur/>"+
		          	"<span class='input-group-btn input-group-hidash-icon'>"+
	                "<i class='fa fa-calendar' aria-hidden='true'></i>"+
	            	"</span>"+
	            	"</p>"+
	            "</div>"+
	          	'<div ng-if="filter.type===\'dropdown\'">'+
		          	'<select ng-model="parameters[$index]" class="form-control">'+
	            		"<option ng-repeat='value in filter.filter_values' value={{value.value}}>{{value.name}}</option>"+ 
	          		'</select>'+
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