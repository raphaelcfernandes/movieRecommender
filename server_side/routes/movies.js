var express = require('express');
var router = express.Router();
var movies = require('../database/models/movie')
var spawn = require("child_process").spawn;
var path = require('path')

router.get('/getAllMovies', function (req, res) {
    movies.find({}).exec().then(function (result) {
        res.status(200).json(result);
    });
});

router.post('/sendRecommendation', function (req, res) {
    req.setTimeout(0);
    const pythonProcess = spawn('python',[path.join(__dirname, '../scripts/recommender.py'),JSON.stringify(req.body)]);
    var finalResult;
    pythonProcess.stdout.on('data', (data) => {
        finalResult = data.toString();
    });
    pythonProcess.stdout.on('close', (data) => {
        console.log(finalResult)
        res.status(200).json(JSON.parse(finalResult));
    });
});

module.exports = router;