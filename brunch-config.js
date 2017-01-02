module.exports = {
  config: {
    paths: {
      watched: ['app'],
      public: './server/static/dist'
    },
    files: {
      javascripts: {
        joinTo: 'js/app.js'
      },
      stylesheets: {
        joinTo: 'css/app.css'
      }
    },
    npm: {
      globals: {
        $: 'jquery',
        jQuery: 'jquery'
      }
    },
    plugins: {
      elmBrunch: {
        outputFolder: 'server/static/dist/js'
      },
      sass: {
        mode: 'native'
      },
      uglify: {}
    }
  }
};
