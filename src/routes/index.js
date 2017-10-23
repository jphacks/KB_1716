var express = require('express');
var router = express.Router();
var uuid = require('node-uuid');
var fs = require('fs');
var execSync = require('child_process').execSync;

var mysql = require('mysql');
var connection = mysql.createConnection({
  host  : 'cocktail.cm9ynyjtyai1.us-east-2.rds.amazonaws.com',
  user  : 'yorechi',
  password  : 'hogehoge123'
});

var multer = require('multer');
var multerStorage = multer.diskStorage({
    destination: function (req, file ,cb) {
    cb(null, './public/uploads');
  },
    filename: function (req, file, cb) {
    cb(null, uuid.v4());
  }
});
var upload = multer({ storage: multerStorage });

router.get('/', function(req, res, next) {
    res.sendfile('./views/index.html');
});

router.post('/', upload.single('upload'), function(req_, res_) {
    var COMMAND = `python ./scripts/facetest.py ./public/uploads/${req_.file.filename}`;

    var result = execSync(COMMAND).toString().split(' ');

    if(result[0] === '-1'){
      res_.render('error2', {error: result[1]});
    }else{
      var QUERY_BF = 'SELECT * FROM sakeDB.hogeTB WHERE color = \"';
      var QUERY_AF = '\"';
      connection.query(QUERY_BF + result[0] + QUERY_AF, function(err,res,fields){
        var rnd = Math.floor( Math.random() * 4 );
        var left = res[rnd]["name"];
        var leftUrl = res[rnd]["srcUrl"];
        var leftText = res[rnd]["messe"];
        connection.query(QUERY_BF + result[1] + QUERY_AF, function(err,res,fields){
          rnd = Math.floor( Math.random() * 4 );
          var right = res[rnd]["name"];
          var rightUrl = res[rnd]["srcUrl"];
          var rightText = res[rnd]["messe"];
          connection.query("SELECT * FROM sakeDB.hogeTB", function(err, res, fields){
            console.log(leftText);
            console.log(rightText);
            res_.render('result', {
              title: 'result',
              file: `/uploads/${req_.file.filename}`,
              left: left,
              leftUrl: leftUrl,
              leftText: leftText,
              right: right,
              rightUrl: rightUrl,
              rightText: rightText
            });
            fs.unlink('/uploads/' + req_.file.filename, function (err){
              console.log(err);
            });
          });
        });
      });
    }
});

module.exports = router;
