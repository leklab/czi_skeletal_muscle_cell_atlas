const path = require('path')
const projectDirectory = path.resolve(__dirname, '..')

const isDev = process.env.NODE_ENV === 'development'

const config = {
  devtool: 'source-map',
  entry: {
    server: [path.resolve(__dirname, './src/server.js')],
  },
  mode: isDev ? 'development' : 'production',
  node: false, // Do not replace Node builtins
  output: {
    path: path.resolve(__dirname, 'dist'),
    publicPath: '/',
    filename: '[name].js',
  },
  optimization: {
    // Define NODE_ENV at run time, not compile time
    // Required because of how the Redis connection is configured in server.js
    nodeEnv: false,
  },
  target: 'node',
}

module.exports = config

