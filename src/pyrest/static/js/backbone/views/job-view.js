/*global Backbone, jQuery, _, ENTER_KEY */
var app = app || {};

(function ($) {
    'use strict';

    // The Application
    // ---------------

    // renders the full list of todo items calling TodoView for each one.
    app.JobView = Backbone.View.extend ({
        el: '#job-view',

        jobTemplate: _.template ($ ('#job-template').html ()),
        messageTemplate: _.template ($ ('#message-template').html ()),


        initialize: function () {
            this.$loading = this.$ ('.job-loading');
            this.$content = this.$ ('.job-content');
//
            this.model.on ('change', this.onChange, this);
//            this.listenTo (this.model.scripts, 'add', this.addOne);
			this.listenTo (this.model.scripts, 'reset', this.addAll);

            this.listenTo (app.appSocket, 'socket-event', this.onSocketEvent);
        },
        events: {
            'click .collapsible-command': 'collapsibleClicked',
            'click .run-script': 'runScript'
        },

        onSocketEvent: function (event, data) {
            var $li = $('#command_'.concat (data.command_id));
            var $code = $('#command_'.concat (data.command_id).concat (' .source'));

            switch (event) {
                case 'command-start':
                    $code.removeClass ('queued');
                    $li.addClass ('running');
                    $li.next().find('.command-output').html('');
                    break;

                case 'command-end':
                    $li.removeClass ('running');


                    var duration = data.end_at - data.start_at;
                    if (duration >= 200)
                        $li.find('.duration-info').removeClass ('hidden').html (duration.toString().concat(' ms'));

                    var exit_code = data.exit_code;
                    if (exit_code != 0)
                        $li.find('.exit-info').removeClass ('hidden').html ('exit: '.concat (exit_code.toString()));

                    // auto-close
                    // $li.next().addClass ('collapsible-closed');
                    break;

                case 'command-output':

                    $li.removeClass ('non-collapsible-command');
                    $li.addClass ('collapsible-command');

                    $li.next().removeClass ('collapsible-closed');
                    $li.next().find ('.'.concat('command-output')).removeClass ('hidden');

                    // add output
                    var $holder = $li.next().find ('.'.concat('command-output'));
                    _.each (data.output, function (r) {
                        $holder.append ('<li class="command-output-' + r.type + '">' + r.line + '</li>');
                    });

                    break;
            }
        },

        render: function () {
            debug ('render job-view');

            this.$el.html (this.jobTemplate (this.model.toJSON ()));
            this.$scripts = this.$ ('.job-scripts');

            this.addAll ();
            return this;
        },

        onChange: function () {
            debug ('onChange job-view model');
            this.render();
            return this;
        },

        collapsibleClicked: function (e) {
            $(e.currentTarget).next().toggleClass ('collapsible-closed');
        },

        runScript: function (ev) {
            var script_id = $(ev.currentTarget).data ('script-id');
            var job_id = this.model.id;
            $('#script_'.concat (script_id).concat (' .script-commands .source')).addClass ('queued');
            $('#script_'.concat (script_id).concat (' .stdout-stderr pre')).html('');
            app.appSocket.sendRunScriptRequest (job_id, script_id);
        },


		addOne: function (script) {
			var view = new app.ScriptView({ model: script });
			this.$scripts.append(view.render().el.innerHTML);
		},

		addAll: function () {
		    debug ('adding scripts');
			this.$scripts.html('');
			this.model.scripts.each (this.addOne, this);
		},
    });
}) (jQuery);