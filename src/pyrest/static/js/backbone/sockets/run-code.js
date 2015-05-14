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
            this.connection.on ('debug', this.onDebug);

            // relay other events
            this.registerEvents (
                'command-output',
                'command-start', 'command-end'
            );
        },


        registerEvents: function () {
            _.each (arguments, function (event, index, args) {
                var ctx = this;
                this.connection.on (event,
                    function (data) {
                        debugSocket (event);
                        console.log (data);
                        ctx.trigger ('socket-event', event, data);
                });
            }, this);
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
            debugSocket ('dbg');
            console.log (msg);
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
                'onConnect', 'onDisconnect', 'registerEvents',
                'sendRunScriptRequest', 'connect'
                );
        }

    }};

    app.appSocket = new app.Socket ({  });
    _.extend(app.appSocket, Backbone.Events);
    app.appSocket.initialize ();


}) (jQuery);