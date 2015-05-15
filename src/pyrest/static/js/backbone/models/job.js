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
            if (!this.scripts)
                this.scripts = new app.ScriptCollection ([], {parse: true});
        },

        parse: function (response) {
            // force initialization
            if (!this.scripts)
                this.initialize ();

            if (_.has (response, "scripts")) {
                this.scripts.reset (response.scripts, {parse: true});
                delete response.scripts;
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
        defaults: {
            id: '',
            exit_code: null,
            start_at: null,
            duration: null
        },

        initialize: function () {
            this.commands = new app.CommandCollection (this.list ? this.list : [], {parse: true});
        },

        parse: function (response) {
           if (_.has (response, "commands")) {
                this.list = response.commands;
                delete response.commands;
            }


            return response;
        },
        toJSON: function () {
            var json = _.clone (this.attributes);
            json.commands = this.commands ? this.commands.toJSON () : [];
            json.startAtRepr = json.start_at ? new Date(json.start_at) : false;
            json.durationRepr = json.duration ? (json.duration/1000.0).toString().concat(' ms') : false;
            json.exitCodeRepr = json.exit_code != 666 ? json.exit_code.toString() : false;
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
            return this.get('source_code').trim().length > 0;
        },

        parse: function (response) {
            return response;
        },
        toJSON: function () {
            var json = _.clone (this.attributes);

            json.hasData = (json.errorLines.length + json.outputLines.length) > 0;
            json.durationRepr = json.duration > 200 ? json.duration + ' ms' : false;
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
