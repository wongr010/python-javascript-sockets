
var WebSocket = require('ws');
wsuri = "ws://127.0.0.1:9000";
sock = new WebSocket(wsuri);

sock.onopen = function () {
 		console.log("Connecting...\n");
  		//sock.send('100'); // Send the message 'Ping' to the server
};

sock.onmessage = function(e) {
	var num=e.data;
	console.log(e.data);
	if (num<90){
		console.log("Good range\n");
	}
	else{
		console.log("Stop!\n");
	}
 
       
    }