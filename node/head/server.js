// Simple GET PUT
// ----------------
// curl -i -X GET http://tardis.local:8001/api
// curl -i -X PUT http://localhost:8001/api --data '{"name":"tom", "age":45.77}' -H "Content-Type: application/json"
// curl -i -X GET http://tardis.local:8001/test.html

var http_debug = require('debug')('k:robot')      // debug
var http = require('http');                  // static web server
var server;                                  // http server
var fs = require('fs');                      // file system
var os = require('os');                      // get system info
// var monitor = require('os-monitor');        // set callbacks for system issues
var jsfile = require('jsonfile');            // read/write config and other things
var program = require('commander');          // command line interface
var chalk = require('chalk');                // color code output in debug

var zmq = require('zmq');                    // comm btwn node and python
var url = require('url');                    // parse in coming urls

var head = function(data){

};

// print some start up stuff
http_debug(chalk.blue(os.hostname()) + ' [' + os.platform() + ']' + os.arch());

// command line options w/ defaults
program
	.version('0.0.1')
// 	.usage('node index.js [options]')
	.description('hi')
	.option('-c, --config <filename>','JSON configuration file','config.json')
	.option('-S, --server <name>','Http server name or address','localhost')
	.option('-P, --port <port>','Http server port',8080)
	.option('-p, --publisher <proto:ip:port>','ZMQ publisher, ex: tcp://127.0.0.1:8000','tcp://*:8080')
	.option('-s, --subscriber <proto:ip:port>','ZMQ subscription, ex: tcp://127.0.0.1:8000','tcp://localhost:8080')
	.parse(process.argv);

http_debug('file',program.config);

// responce for an error ... not supported
var apiError = function(res,str){
	res.writeHead(405, "Method not supported", {'Content-Type': 'text/html'});
	res.write(str);
	res.end();
	return res;
}

// responce for a good request
var apiGood = function(res,str){
	res.writeHead(200, "OK", {'Content-Type': 'text/html'});
	res.write(str);
	res.end();
	return res;
}

var send404 = function(res){
    res.writeHead(404);
    res.write('404 File Not Found');
    res.end();
};

server = http.createServer(function(req, res){
    var path = url.parse(req.url).pathname;
    http_debug( path );
//     http_debug( req );
	// if (path == '/api'){
	// 	// if (req.method == 'PUT') {
	// 	// 	var ans = '';
	// 	//
	// 	// 	req.on('data', function(chunk) {
	// 	// 		http_debug(chunk.toString());
	// 	// 		ans = head(chunk.toString());
	// 	// 	});
	// 	//
	// 	// 	res = apiGood(res,ans);
	// 	// }
	// 	if (req.method == 'GET') {
	// 		var query = url.parse(req.url).query;
	//
	// 		if (query == 'system=cpu'){
	// 			res = apiGood(res,'system info: ' + JSON.stringify(os.networkInterfaces()) + ' ' + JSON.stringify(os.cpus()) );
	// 		}
	// 		else {
	// 			res = apiError(res,'??');
	// 		}
	// 	}
	// 	// force users to use GET/PUT
	// 	else {
	// 		res = apiError(res,"Wrong method: use GET/PUT\n");
	// 		http_debug("Wrong method " + req.method);
	// 	}
	// }
	if (path == '/'){
		http_debug(__dirname);
		fs.readFile(__dirname + '/face.htm', function(err, data){
                if (err){
                    return send404(res);
                }
                res.writeHead(200, {'Content-Type': path == 'json.js' ? 'text/javascript' : 'text/html'});
//                 res.writeHead(200, {'Content-Type':'text/html'});
                res.write(data, 'utf8');
                res.end();
            });
	}
	else {
		// force users to /api
		http_debug("Wrong path " + path);
		apiError(res,"Wrong path: use http://host/api\n");
	}
});




//[ socket.io ]////////////////////////////////////////////////
var io = require('socket.io').listen(server);       // comm btwn node and browser
io.on('connection', function(socket){
	socket.on('client_data', function(data){
		http_debug("socket.io Rx: " + JSON.stringify(data));
	});

	socket.on('disconnect', function(){
		http_debug('socket.io disconnect');
	});

// 	socket.on('connect', function(){
// 		http_debug('socket.io connect');
// 	});
});

// setInterval(function(){
// 	http_debug('socket.io sending message');
// }, 1000);

// save data in json form to a file
// var saveInfo = function(filename,json){
// 	jsonfile.writeFile(filename, json, function (err) {
// 		http_debug(chalk.red(err));
// 	});
// }

http_debug( 'Starting server on: '+program.server+' '+program.port );
server.listen(program.port,program.server);

//[ ZMQ ]//////////////////////////////////////////////////////////////////////

// var sub = zmq.socket('sub');
// sub.subscribe('b');
// // http_debug('Subscriber connected to port ' + program.subscriber);
// sub.on('message', function(message,t) {
// 	var m=JSON.parse(t);
// 	http_debug('sub get message: ' + message + ' '+ m['a']);
// });
// sub.identity = 'sub:' + process.pid;
// sub.on('connect', function(fd, ep) {
// 	http_debug('sub connect to: ' + ep);
// });
// sub.on('disconnect', function(fd, ep) {
// 	http_debug('sub disconnect to: ' + ep);
// });
// sub.monitor();
// sub.connect(program.subscriber);
//
//
// var pub = zmq.socket('pub');
// pub.identity = 'pub:' + process.pid;
// pub.bind(program.publisher, function(err) {
// 	if (err) {
// 		http_debug('Pub: ' + err);
// // 		pub.bind('tcp://localhost:8080');
// 	}
// 	else {
// 		http_debug('Publisher connected: ' + program.publisher);
// 	}
// });
//
// setInterval(function(){
// 	http_debug('pub sending message');
// 	var d = JSON.stringify({"a":21,"b":22});
// 	pub.send('a '+' ho regular ' + pub.identity);
// 	pub.send(['b',d]);
// }, 1000);
