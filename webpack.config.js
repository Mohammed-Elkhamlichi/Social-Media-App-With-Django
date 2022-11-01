const path = require('path')

module.exports = {
    mode:'development',
    entry: './theme/static/js/index.js',
    output: {
        filename:"bundle.js",
        path: path.resolve(__dirname,'theme/static/js')
    }
}