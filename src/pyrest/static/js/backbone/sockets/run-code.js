/*global Backbone, jQuery, _, ENTER_KEY */
var app = app || {};

(function ($) {
    'use strict';

    app.Socket = function (obj) { return {

        // socket connection
        connection: null,

        uponConnection: [],

        // socket url
        url: "http://" + document.domain + ":" + location.port + "/",


        connect: function () {
            this.connection = io.connect (this.url);

            // register events
            this.connection.on ('connect', this.onConnect);
            this.connection.on ('disconnect', this.onDisconnect);
            this.connection.on ('command-start', this.onCommandStart);
            this.connection.on ('command-end', this.onCommandEnd);
            this.connection.on ('stdout', this.onStdout);
            this.connection.on ('stderr', this.onStderr);
            this.connection.on ('debug', this.onDebug);
        },

        sendRunScriptRequest: function (job_id, script_id) {
            debug ('sendRunScriptRequest');
            if (this.connection === null) {
                this.uponConnection = [this.sendRunScriptRequest, job_id, script_id];

                this.connect ();
                return this;
            }

            this.connection.emit ('run-code', {job_id: job_id, script_id: script_id});
        },

        onConnect: function () {
            debugSocket ('CONNECTED');
            if (this.uponConnection && this.uponConnection.length > 0) {

                var args = _.clone (this.uponConnection);
                this.uponConnection = null;
                var func = args.shift();
                func.apply (this, args);
            }

        },

        onDisconnect: function () {
            debugSocket ('DISCONNECTED');
        },

        onDebug: function (msg) {
//            debugSocket (msg);
        },

        onCommandStart: function (msg) {
//            console.log (msg);
            this.trigger ('socket-event', msg, this);
        },

        onCommandEnd: function (msg) {
//            console.log (msg);
        },

        onStdout: function (msg) {
//            console.log (msg);
        },

        onStderr: function (msg) {
//            console.log (msg);
        },


        initialize: function () {
            _.bindAll (this,
                'onConnect', 'onDisconnect', 'onDebug',
                'sendRunScriptRequest', 'connect',
                'onCommandStart', 'onCommandEnd', 'onStdout', 'onStderr'
                );
        }

    }};

    app.appSocket = new app.Socket ({  });
    _.extend(app.appSocket, Backbone.Events);
    app.appSocket.initialize ();


}) (jQuery);