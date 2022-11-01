const path = require("path");

module.exports = {
    mode: "production",
    entry: "./theme/static/js/index.js",
    output: {
        filename: "bundle.js",
        path: path.resolve(__dirname, "theme/static/js"),
    },
};
