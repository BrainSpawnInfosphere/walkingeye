// get system info and return a dictionary of info
var debug = require('debug')('kevin:syslib');
var os = require('os');
var osxRelease = require('osx-release');
var fs = require('fs');

var disk = require('../lib/diskinfo.js');
var diskinfo = {};


disk.getStorage(function(err, drives) {
	if(err){ debug('err: '+err); }
	  for (var key in drives) {
//			   console.log('Drive ' + key + ': ' + drives[key].available + ' / ' + drives[key].size + ' free, ' + drives[key].capacity + ' used');
		diskinfo[key] = { "available":drives[key].available, "size":drives[key].size, "capacity":drives[key].capacity };
	  }
});

function getIP(){
	// Get ip info from interface e
	function ip(e){
		var ans = {};
		for( var i=0; i < net[e].length; i++){
			if(net[e][i]['family'] == 'IPv4'){
				ans['IPv4'] = {'address': net[e][i]['address'], 'mac': net[e][i]['mac']};
			}
			else if(net[e][i]['family'] == 'IPv6'){
				ans['IPv6'] = {'address': net[e][i]['address'], 'mac': net[e][i]['mac']};
			}
		}
		return ans;
	}
	var net = os.networkInterfaces();

	// determine interface based on system type
	switch( os.type().toLowerCase() ){
		case 'linux':
			if (net['eth0']) return ip('eth0');
			if (net['eth1']) return ip('eth1');
			if (net['wlan0']) return ip('wlan0');
			if (net['wlan1']) return ip('wlan1');
			break;
		case 'darwin':
			if (net['en0']) return ip('en0');
			if (net['en1']) return ip('en1');
			break;
		default:
			if (net['lo0'])return ip('lo0');
			if (net['lo'])return ip('lo');
	}
}

// find uptime
function secondsToTime() {
	var sec = os.uptime();
	var d = parseInt(Math.floor(sec/(3600*24)));
	var h = parseInt(Math.floor(sec%(3600*24)/3600));
	var m = parseInt(Math.floor((sec%(3600*24))%3600)/60);
	return d+' days '+h+' hrs '+m+' mins';
}

// convert bytes to proper size
function bytesToSize(bytes) {
   var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
   if (bytes == 0) return '0 Byte';
   var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
   return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
}

// main function exported, returns json of system info
exports.sysinfo = function(){
	// system info
	var sys = {'platform': os.platform(),
				'load': os.loadavg()[0].toFixed(2),
				'release': os.release(),
				'uptime': secondsToTime(),
				'free_memory': bytesToSize(os.freemem()),
				'total_memory': bytesToSize(os.totalmem()),
				'cpu': os.cpus()[0]['model'],
				'arch': os.arch(),
				'hostname':os.hostname(),
				'network': getIP(),
				'storage': diskinfo,
				'timestamp': new Date()
				};

	// platform fixes
	if (sys['platform'] == 'darwin') {
		sys['platform'] = 'OSX';
		sys['release'] = osxRelease(sys['release']); // {name: 'Mavericks', version: '10.9'}
	}
	// for linux, read /etc/os-release and find the PRETTY name
	else if (sys['platform'] == 'linux') {
		try {
			var file = fs.readFileSync('/etc/os-release','utf8').split('\n');
			var name = '';
			for (var i = 0; i < file.length; i++){
				if( file[i].indexOf('PRETTY') >= 0 ){
					name = file[i].split('=')[1];
					name = name.replace(/"/g,'');
					break;
				}
			}
			sys['platform'] = 'Linux';
			sys['release'] = {'name': name, 'version': os.release()};
		}
		catch(err){
			debug('WARNING: /etc/os-release not found');
			debug(err);
			sys['platform'] = 'Linux';
			sys['release'] = {'name': 'Linux', 'version': os.release()};
		}
	}
	else {
		sys['platform'] = os.platform();
		sys['release'] = {'name': os.platform(), 'version': os.release()};
	}

	return sys;
};

// used by real-time update to grab a smaller sub set of info that changes
exports.simpleInfo = function(){

	// system info
	var sys = {'load': os.loadavg()[0].toFixed(2),
				'uptime': secondsToTime(),
				'free_memory': bytesToSize(os.freemem()),
				'total_memory': bytesToSize(os.totalmem()),
				'timestamp': new Date()
				};
	return sys;
}
