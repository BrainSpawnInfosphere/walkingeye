// Create an HTML5 webpage 

function line(a,b,c){
	return '<tr><td class="bold">' + a + '</td><td id="' + c + '">' + b + '</td></tr>';
}

function table(info){
	var t = '<table class="center">';
	t += line(info['platform'],info['release']['name']+'('+info['release']['version']+')');
	t += line('CPU',info['cpu']);
	t += line('Arch',info['arch']);
	t += line('Load',info['load'],'load');
	t += line('Memory',info['free_memory']+' / '+info['total_memory'],'mem');
	t += line('Uptime',info['uptime'],'up');
	t += line('IPv4',info['network']['IPv4']['address']+' / '+info['network']['IPv4']['mac']);
	t += line('IPv6',info['network']['IPv6']['address']+' / '+info['network']['IPv6']['mac']);
	t += line('Storage','');
	for (var key in info['storage']){
		t += line(key + ':', info['storage'][key].available + ' of ' + info['storage'][key].size + ' free, ' + info['storage'][key].capacity + ' used');
	}
	t += '</table>';
	return t;
}

module.exports = function(info,realtime){
	var page = '<!DOCTYPE html><html>';
	page += '<head>';

if (realtime) {
	page += '<script src="/socket.io/socket.io.js"></script>';
	page += '<script>';
	page += 'var socket = io();';
	page += 'socket.on("data", function(data) {';
	page += '  document.getElementById("mem").innerHTML = data["freemem"];';
	page += '  document.getElementById("load").innerHTML = data["load"];';
	page += '  document.getElementById("up").innerHTML = data["up"];';
	page += '  document.getElementById("timestamp").innerHTML = data["timestamp"];';
	page += '});';
	page += '</script>';
}

	page += '<style>';
	page += 'table.center { margin-left:auto; margin-right:auto;}';
	page += 'td.bold {font-weight: bold; text-align: right;}';
	page += 'h1.center {text-align: center;}';
	page += 'div.center {text-align: center;}';
	page += 'div.footer {position: fixed; bottom: 0; width: 100%; height: 44px; line-height: 44px; text-align: center; background-color: #888888;}';
	page += 'a {display: inline-block; margin: 0 40px; text-decoration: none; color: #ffffff; text-transform: uppercase; font-size: 12px;}';
	page += '</style>';
	page += '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">';
	page += '</head>';
	page += '<body>';

	// OS picture
	page += '<div class="center">';
	if (info['platform'] == 'OSX') {page += '<i class="fa fa-apple fa-5x"></i>';}
	else {page += '<i class="fa fa-linux fa-5x"></i>';}
	page += '</div>';

	page += '<h1 class="center">'+ info['hostname']+'</h1>'; 
	page += table(info); 
	page += '<div class="footer">';
	page += '<a href="https://github.com/walchko"> <i class="fa fa-github fa-lg"></i> Github</a> ';
	page += '<a id="timestamp">' + info['timestamp'] + '</a>';
	page += '<a href="qr"> <i class="fa fa-qrcode fa-lg"></i> </a>';
	page += '</div>';
	page +='</body></html>';
	return page;
};