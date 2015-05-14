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

        parse: function (response) {

        // detect broken link and return 'broken' model for view to show
            if (_.has (response, "scripts")) {
                this.scripts = new app.ScriptCollection (response.scripts, {parse: true});
                delete response.scripts;
            } else {
                this.scripts = new app.ScriptCollection ([], {parse: true});
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

        parse: function (response) {
            if (_.has (response, "commands")) {
                this.commands = new app.CommandCollection (response.commands, {
                    parse: true
                });
                delete response.commands;
            }
            return response;
        },
        toJSON: function () {
            var json = _.clone (this.attributes);
            json.commands = this.commands ? this.commands.toJSON () : [];
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
