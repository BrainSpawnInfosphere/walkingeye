// create a QR image from host info

// var qr = require('qr-image');

// module.exports = function(info){
// 	var data = {};
//
// 	data.hostname = info['hostname'];
// 	data.ipv4 = info['network']['IPv4']['address'];
// 	data.mac = info['network']['IPv4']['mac'];
// 	data.ipv6 = info['network']['IPv6']['address'];
//
// 	var img = qr.image(JSON.stringify(data));
//
// 	return img;
// };

var u = new SpeechSynthesisUtterance();

exports.simpleInfo = function(txt){
    // var u = new SpeechSynthesisUtterance();
    u.text = txt;
    u.lang = 'en-UK';
    u.rate = 1.2;
    // u.onend = function(event) { alert('Finished in ' + event.elapsedTime + ' seconds.'); }
    speechSynthesis.speak(u);
}
