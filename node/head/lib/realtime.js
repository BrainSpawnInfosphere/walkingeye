// update web page with real-time info using socket.io

var sysinfo = require('./sysinfo.js');

var io;

module.exports = function(server,dt){
	io = require('socket.io').listen(server);
		
	// send data
	setInterval(sendData, dt);
};

function sendData(){
// 	console.log('clients: '+ io.engine.clientsCount);
	if( io.engine.clientsCount < 1 ){ return; }
	var info = sysinfo.simpleInfo();
	io.emit('data', { 'freemem': info['free_memory']+' / '+info['total_memory'], 'load': info.load, 'up': info.uptime, 'timestamp': info.timestamp });
}
