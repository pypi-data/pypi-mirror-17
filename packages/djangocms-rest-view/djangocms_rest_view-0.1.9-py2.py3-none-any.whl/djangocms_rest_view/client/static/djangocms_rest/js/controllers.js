var restControllers = angular.module('cmsrest.controllers', []);

restControllers.controller('ClientCtrl', ['$scope', '$location', '$routeParams', 'restClient', function ($scope, $location, $routeParams, restClient) {

  restClient.boot();

  restClient.getPagesMenu()
    .then(function (res) {
      $scope.menu = res.data;
      if (res.data.length > 0) {
        $location.path('/pages/' + ($routeParams.pageId || res.data[0].id));
      }
    })

}]);


restControllers.controller('PageDetailCtrl', ['$scope', '$location', '$window', '$routeParams', 'restClient', function ($scope, $location, $window, $routeParams, restClient) {
  $scope.content_page;
  $scope.sekizais;

  LOAD_JS_FILE = 0;
  LOAD_JS_SCRIPT = 1;
  LOAD_CSS_FILE = 2;

  var sekizaiConfig = {
    'js-media': {
      'action': LOAD_JS_FILE,
      'source': 'media'
    },
    'css-media': {
      'action': LOAD_CSS_FILE,
      'source': 'media'
    },
    'css-screen': {
      'action': LOAD_CSS_FILE,
      'source': 'static'
    },
    'script_ready': {
      'action': LOAD_JS_SCRIPT
    },
    'js': {
      'action': LOAD_JS_SCRIPT
    },
    'js-script': {
      'action': LOAD_JS_FILE,
      'source': 'static'
    },
  }

  $scope.finishLoading = function() {
    setTimeout(function () {
        $(document).ready(function() {
          restClient.loadSekizaiResources(
            $scope.sekizais, sekizaiConfig
          );
      });

      $('div[ng-view] a:not(no-rest)').click(function() {
        var local_event = event;
        local_event.preventDefault();
        var href = $(this).attr('href');
        var that = this;
        restClient.rewriteUrl(href)
          .then(function (newUrl) {
            $location.path(newUrl);
          }, function (newUrl) {
            this.dispatchEvent(local_event);
          });

      });
    }, 100);
  };

  restClient.getPage($routeParams.pageId)
    .then(function (res_data) {
      var load_event = new Event('page-load');
      this.dispatchEvent(load_event);
      $scope.templateUrl = '/static/partials/' + res_data.data.template;
      $scope.sekizais = res_data.data.placeholders.sekizai;
      $scope.content_page = res_data.data;
    }, function() {});
}]);
