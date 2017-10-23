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

/* GET home page. */
router.get('/', function(req, res, next) {
  //res.render('index', { title: 'Express' });
  res.sendfile('./views/index.html');
});

router.post('/', upload.single('upload'), function(req, res_) {
  var COMMAND = `python ./scripts/facetest.py ./public/uploads/${req.file.filename}`;

  var result = execSync(COMMAND).toString().split(' ');

  if(result[0] === '-1'){
    res_.render('error2', {error: result[1]}); //人数によって変動
  }else{
    //connection.connect(function(err) {
    //  if(err){
    //    console.error('error connecting: ' + err.stack);
    //    return;
    //  }
    //  console.log('connected as id ' + connection.threadId);
    //});
    connection.query('SELECT * FROM sakeDB.hogeTB WHERE color = \"' + result[0] + `\"`, function(err,res,fields){
      var left = res[0]["name"];
      var leftUrl = res[0]["srcUrl"];
      var leftText = res[0]["messe"];
	    connection.query('SELECT * FROM sakeDB.hogeTB WHERE color = \"' + result[1] + `\"`, function(err,res,fields){
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
		    //fs.unlink(req.file, function (err){
		    //  console.log(err);
		    //});
		});
	    });
    });
  }


});

module.exports = router;
