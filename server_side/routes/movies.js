var express = require('express');
var router = express.Router();
var movies = require('../database/models/movie')
var spawn = require("child_process").spawn;
var path = require('path')

router.get('/getAllMovies', function (req, res) {
    movies.find({}).limit(100).exec().then(function (result) {
        res.status(200).json(result);
    });
});

router.post('/sendRecommendation', function (req, res) {
    const pythonProcess = spawn('python',[path.join(__dirname, 'teste.py')]);
    pythonProcess.stdout.on('data', (data) => {
        console.log(data.toString())
    })
});

module.exports = router;