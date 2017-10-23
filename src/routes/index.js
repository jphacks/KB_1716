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

router.post('/', upload.single('upload'), function(req, res_) {
    var COMMAND = `python ./scripts/facetest.py ./public/uploads/${req.file.filename}`;

    var result = execSync(COMMAND).toString().split(' ');

    if(result[0] === '-1'){
      res_.render('error2', {error: result[1]});
    }else{
      console.log("test");
      var QUERY_BF = 'SELECT * FROM sakeDB.hogeTB WHERE color = \"';
      var QUERY_AF = '\"';
      connection.query(QUERY_BF + result[0] + QUERY_AF, function(err,res,fields){
        console.log(res);
        var left = res[0]["name"];
        var leftUrl = res[0]["srcUrl"];
        var leftText = res[0]["messe"];
        connection.query(QUERY_BF + result[1] + QUERY_AF, function(err,res,fields){
          var right = res[0]["name"];
          var rightUrl = res[0]["srcUrl"];
          var rightText = res[0]["messe"];
          connection.query("SELECT * FROM sakeDB.hogeTB", function(err, res, fields){
            console.log(leftText);
            console.log(rightText);
            res_.render('result', {
              title: 'result',
              file: `/uploads/${req.file.filename}`,
              left: left,
              leftUrl: leftUrl,
              leftText: leftText,
              right: right,
              rightUrl: rightUrl,
              rightText: rightText
            });
          fs.unlink(req.file, function (err){
            console.log(err);
          });
          });
        });
      });
    }
});

module.exports = router;
