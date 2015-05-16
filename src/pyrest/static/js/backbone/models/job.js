var app = app || {};

(function () {
    'use strict';

    // Job Model
    // ----------

    app.Job = Backbone.Model.extend ({


        // load data
        urlRoot: '/api/jobs/',

        // Default attributes
        defaults: {
            id: '',
            name: '',
            status: '',
            settings: {},
            user: {}
        },

        initialize: function () {
            this.scripts = new app.ScriptCollection (this.list ? this.list : [], {parse: true});
        },

        parse: function (response) {
            // force initialization
            if (!this.scripts)
                this.initialize ();

            if (_.has (response, "scripts")) {
                this.list = response.scripts;
                this.list.sort(function (a, b) {
                    return a.start_at - b.start_at;
                });
                delete response.scripts;


                if (this.scripts)
                    this.scripts.reset (this.list, {parse: true});
            }

            return response;
        },
        toJSON: function () {
            var json = _.clone (this.attributes);
            json.scripts = this.scripts ? this.scripts.toJSON () : [];
            return json;
        }
    });

    app.Script = Backbone.Model.extend ({

        // load data
        urlRoot: '/api/scripts/',

        defaults: {
            id: '',
            exit_code: null,
            start_at: 0,
            duration: null
        },

        initialize: function () {
            this.commands = new app.CommandCollection (this.list ? this.list : [], {parse: true});
        },

        parse: function (response) {
            if (_.has (response, "commands")) {
                this.list = response.commands;
                delete response.commands;

                if (this.commands)
                    this.commands.reset (this.list, {parse: true});
            }

            return response;
        },
        toJSON: function () {
            var json = _.clone (this.attributes);
            json.commands = this.commands ? this.commands.toJSON () : [];
            json.startAtRepr = json.start_at ? formatDate (json.start_at) : false;
            json.durationRepr = json.duration ? (json.duration / 1000.0).toString ().concat (' ms') : false;
            json.exitCodeRepr = json.exit_code !== null && json.exit_code != 666 ? json.exit_code.toString () : false;
            json.commandsRaw = '';
            _.each (json.commands, function (command) {
                json.commandsRaw += command.source_code + '\n';
            });
            return json;
        }
    });

    app.Command = Backbone.Model.extend ({
        defaults: {
            id: '',
            duration: null,
            outputLines: [],
            errorLines: [],
            exit_code: null,
            source_code: null
        },

        isValid: function () {
            return this.get ('source_code').trim ().length > 0;
        },

        parse: function (response) {
            return response;
        },
        toJSON: function () {
            var json = _.clone (this.attributes);

            json.hasData = (json.errorLines.length + json.outputLines.length) > 0;
            json.durationRepr = json.duration > 200 ? json.duration + ' s' : false;
            json.exitCodeRepr = json.exit_code !== null && json.exit_code != 0 ? 'exit: ' + json.exit_code : false;
            return json;
        }
    });

    app.ScriptCollection = Backbone.Collection.extend ({
        model: app.Script
    });
    app.CommandCollection = Backbone.Collection.extend ({
        model: app.Command
    });
}) ();
