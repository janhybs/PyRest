/*global Backbone, jQuery, _, ENTER_KEY */
var app = app || {};

(function ($) {
    'use strict';

    // The Application
    // ---------------

    // renders the full list of todo items calling TodoView for each one.
    app.ScriptView = Backbone.View.extend ({
        tagName: 'div',

        jobTemplate: _.template ($ ('#script-template').html ()),

        initialize: function () {
            this.model.on ('sync', this.onSync, this);
            this.commandViews = [];
            this.commandCompleted = 0;

            this.listenTo (app.appSocket, 'script-start:' + this.model.id, this.onScriptStart);
            this.listenTo (app.appSocket, 'script-end:' + this.model.id, this.onScriptEnd);
            this.listenTo (app.appSocket, 'command-end', this.onCommandEnd);
        },

        destroy: function () {
            this.remove ();
            this.destroyChildren ();
        },

        destroyChildren: function () {
            _.each (this.commandViews, function (view) {
                view.destroy ();
            });
            this.commandViews = [];
        },

        events: {
            'click .run-script': 'runScript',
            'click .edit-script': 'editScript',
            'click .save-changes': 'saveChanges'
        },


        render: function () {
            this.$el.html (this.jobTemplate (this.model.toJSON ()));
            this.$commands = this.$el.find ('.script-commands');

            this.addAll ();
            return this;
        },

        addOne: function (command) {
            if (!command.isValid ())
                return this;

            var view = new app.CommandView ({model: command});
            this.commandViews.push (view);
            this.$commands.append (view.render ().el);
            return this;
        },

        addAll: function () {
            this.destroyChildren ();
            this.$commands.html ('');
            this.model.commands.each (this.addOne, this);
        },


        runScript: function (ev) {
            this.$ (' .script-commands .source').addClass ('queued');
            this.$ (' .stdout-stderr pre').html ('');
            app.appSocket.sendRunScriptRequest (this.model.id);
        },

        editScript: function (ev) {
            this.$ ('.script-commands').hidden ();
            this.$ ('.script-info').hidden ();
            this.$ ('.script-details').hidden ();
            this.$ ('.script-editable-commands').visible ();
        },

        saveChanges: function (ev) {
            this.$ ('.script-commands').visible ();
            this.$ ('.script-info').visible ();
            this.$ ('.script-details').visible ();
            this.$ ('.script-editable-commands').hidden ();

            var raw = this.$ ('.script-editable-commands textarea').val ();

            // virgin script will be edited
            if (this.model.get ('exit_code') == 666) {
                var that = this;
                this.model.set ({commandsNew: raw});
                Backbone.sync ('update', this.model, {
                    success: function (data) {
                        that.model.fetch ();
                    },
                    error: function () {
                        console.log ('model NOT updated');
                    }
                });
            } else {
                // executed scripts will be added
                var model = new app.Script ({commandsNew: raw, job_id: this.model.get ('job_id')});
                Backbone.sync ('create', model, {
                    success: function (data) {
                        //app.job.isLoading = true;
                        //app.job.isBroken = false;
                        //app.jobView.render();
                        //
                        //app.job.fetch ({
                        //    success: function () {
                        //        app.job.isLoading = false;
                        //        app.job.isBroken = false;
                        //        app.jobView.render();
                        //    },
                        //    error: function () {
                        //        app.job.isLoading = false;
                        //        app.job.isBroken = true;
                        //        app.jobView.render();
                        //    }
                        //});
                        app.job.fetch()
                    },
                    error: function () {
                        console.log ('model NOT created');
                    }
                });
            }

        },

        onSync: function () {
            this.render ();
        },

        onScriptStart: function (data) {
            this.$ ('.progress').removeClass ('hidden');
            this.$ ('.progress-bar').css ('width', '0%').attr ('aria-valuenow', 0);
            this.commandCompleted = 0;
        },

        onScriptEnd: function (data) {
            this.$ ('.progress').addClass ('hidden');
            this.model.set ({exit_code: data.exit_code, duration: data.duration, start_at: data.start_at});
        },


        onCommandEnd: function (data) {
            // event is not for me
            if (data.script_id != this.model.id) return;

            var value = (++this.commandCompleted / this.commandViews.length) * 100;
            value = value > 100 ? 100 : value < 0 ? 0 : value;
            this.$ ('.progress-bar').css ('width', value + '%').attr ('aria-valuenow', value);
        },
    });
}) (jQuery);