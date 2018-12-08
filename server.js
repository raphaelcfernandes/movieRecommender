var express = require("express");
var bodyParser = require("body-parser");
var cors = require('cors');
var path = require('path');
var cookieParser = require('cookie-parser');
const api = require('./server_side/routes')
const mongoose = require('mongoose');
const config = require('./server_side/database/config')
const http = require('http');
const app = express();
const port = process.env.PORT || 8080;

mongoose.connect(config.database, { useNewUrlParser: true }, function (err, db) {
    if (err) { return console.dir(err); }
    else {
        console.log("mongoDB connected.");
    }
});

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'dist')));
app.use(api)

const server = http.createServer(app);
server.listen(port, () => console.log(`API running on localhost:${port}`));

module.exports = app;

