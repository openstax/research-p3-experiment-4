var path = require('path');
var webpack = require('webpack');

// Third party plugins.
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var ManifestRevisionPlugin = require('manifest-revision-webpack-plugin');

// Development asset host, asset location and build output path.
var publicHost = 'http://localhost:2992';
var rootAssetPath = path.join(__dirname, 'digital_logic/static');
var cssAssetPath = rootAssetPath + '/css';
var buildOutputPath = path.join(__dirname, 'digital_logic/build/public');


module.exports = {
  entry: {
    // Chunks (files) that will get written out for JS and CSS files.
    app: [
      rootAssetPath + '/js/src/index.js',
      cssAssetPath + '/style.css'
    ]
  },
  output: {
    // Where and how will the files be formatted when they are output.
    path: buildOutputPath,
    publicPath: publicHost + '/static/',
    filename: '[name].js'
  },
  devServer: {
    // Proxy requests to the API server that the
    // webpack-dev-server can't satisfy.
    host: 'localhost',
    proxy: {
      '*': {
        target: 'http://127.0.0.1:5000',
        secure: false
      }
    },
    watchOptions: {
      poll: 500,
      ignored: /node_modules/
    }
  },
  resolve: {
    // Avoid having to require files with an extension if they are here.
    extensions: ['', '.js', '.jsx', '.css'],
    alias: {
      'jquery': path.resolve(__dirname, 'node_modules/jquery/dist/jquery.js')
    }
  },
  module: {
    // Various loaders to pre-process files of specific types.
    // If you wanted to SASS for example, you'd want to install this:
    //   https://github.com/jtangelder/sass-loader
    loaders: [
      {
        test: /\.jsx?$/i,
        loaders: ['babel-loader'],
        exclude: /node_modules/
      },
      {
        test: /\.scss$/i,
        loader: ExtractTextPlugin.extract('style-loader', 'sass-loader')
      },
      {
        test: /\.css$/i,
        loader: ExtractTextPlugin.extract('style-loader', 'css-loader')
      },
      {
        test: /\.(jpe?g|png|gif|svg([\?]?.*))$/i,
        loaders: [
          'file?context=' + rootAssetPath + '&name=[path][name].[ext]',
          'image?bypassOnDebug&optimizationLevel=7&interlaced=false'
        ]
      },
      {
        test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        loader: "url?limit=10000&mimetype=application/font-woff"
      },
      {
        test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        loader: "file"
      }
    ]
  },
  plugins: [
    // Stop modules with syntax errors from being emitted.
    new webpack.NoErrorsPlugin(),
    // Ensure CSS chunks get written to their own file.
    new ExtractTextPlugin('[name].css'),
    // Create the manifest file that Flask and other frameworks use.
    new ManifestRevisionPlugin(path.join('digital_logic', 'build', 'manifest.json'), {
      rootAssetPath: rootAssetPath,
      ignorePaths: ['/js', '/css', '/img']
    }),
    new webpack.ProvidePlugin({
      $: "jquery",
      jquery: "jquery"
    })
  ]
};
