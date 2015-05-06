var app = app || {};

(function () {
    'use strict';

    // Job Model
    // ----------

    // Our basic **Todo** model has `title`, `order`, and `completed` attributes.
    app.Job = Backbone.Model.extend ({


        // load data
        urlRoot: 'data/',

        // Default attributes for the todo
        // and ensure that each todo created has `title` and `completed` keys.
        defaults: {
            name: '',
            status: '',
            settings: {},
            user: {}
        },

        parse: function (response) {
            if (_.has (response, "scripts")) {
                this.scripts = new app.ScriptCollection (response.scripts, {
                    parse: true
                });
                delete response.scripts;
            }
            return response;
        },
        toJSON: function () {
            var json = _.clone (this.attributes);
            json.scripts = this.scripts.toJSON ();
            return json;
        }

        //
        //initialize: function () {
        //    this.set("scripts", new app.User());
        //}
        //// Toggle the `completed` state of this todo item.
        //toggle: function () {
        //    this.save({
        //        completed: !this.get('completed')
        //    });
        //}
    });

    app.Script = Backbone.Model.extend ({
        defaults: {
            duration: '',
            result: '',
            timestamp: ''
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
            json.commands = this.commands.toJSON ();
            return json;
        }
    });

    app.Command = Backbone.Model.extend ({
        defaults: {
            duration: '',
            output: '',
            error: '',
            source_code: ''
        }
    });

    app.ScriptCollection = Backbone.Collection.extend ({
        model: app.Script
    });
    app.CommandCollection = Backbone.Collection.extend ({
        model: app.Command
    });
}) ();
