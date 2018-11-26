const express = require('express')
const router = express.Router();

router.use('/movies', require('./movies'))

// router.get('/', (req, res) => {
//     res.send("api works!");
// });


module.exports = router;