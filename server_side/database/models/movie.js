var mongoose = require('mongoose')
var Schema = mongoose.Schema;

var Movie = new Schema({
    movieId: Number,
    year: Number,
    title: String,
    genres: Array
});

module.exports = mongoose.model('Movie', Movie)

// module.exports.getAllMovies = (callback) => {
// 	Movies.find(callback);
// }