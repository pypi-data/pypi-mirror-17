//jshint strict: false
module.exports = function(config) {
  config.set({

    basePath: 'casepropods/family_connect_subscription',

    files: [
      'karma/vendor/angular.min.js',
      'karma/vendor/angular-mocks.js',
      'sitestatic/subscription_pod_template.html',
      'karma/init.js',
      'sitestatic/subscription_pod_directives.js',
      'karma/test-pod.coffee',
    ],

    frameworks: ['jasmine'],

    preprocessors: {
          '**/*.coffee': ['coffee'],
          'sitestatic/*.html': ['ng-html2js']
        },
        
    ngHtml2JsPreprocessor: {
      moduleName: 'templates'
    },


    browsers: ['PhantomJS'],

    reporters: ['progress'],

    port: 9876,
    colors: true,
    logLevel: config.LOG_INFO,
    autoWatch: false,
    singleRun: false,
  });
};
