var app = app || {};
var now = Date.now();

function debug (msg) {
    var time = (Date.now() - now).toString();
    while (time.length < 5) time = " " + time;
    console.log (time + ': ' + msg);
}

function debugSocket (msg) {
    debug ('[s]: ' + msg);
}
$ (function () {
    'use strict';


    //$.ajax('http://localhost/jsapp/data/job-1.json', function ())
    //console.log (app.ScriptCollection.url)


    // kick things off by creating the `App`
	app.appView = new app.AppView();
	Backbone.history.start();


	window.socketConnect = function () {
	    var url = "http://" + document.domain + ":" + location.port;
        var socket = io.connect(url + "/");

        socket.on('connect', function() {
            debugSocket ('CONNECTED');

            socket.emit ('run_code', {msg: 'fooo'});
        });
        socket.on('disconnect', function() {
            debugSocket ('DISCONNECTED');
            socket.disconnect();
        });
        socket.on('debug', function(msg) {
            debugSocket (msg);
        });
	}



});