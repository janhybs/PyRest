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

            this.model.on ('change', this.onChange, this);
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

                case 'stdout':
                case 'stderr':

                    $li.removeClass ('non-collapsible-command');
                    $li.addClass ('collapsible-command');

                    $li.next().removeClass ('collapsible-closed');
                    $li.next().find ('.'.concat(event)).removeClass ('hidden');
                    $li.next().find ('.'.concat(event)).append ('<li>' + data[event] + '</li>');
                    break;
            }
        },

        render: function () {
            if (this.model.isLoading)
                return this.$el.html (this.messageTemplate ({message: 'Loading job details', type: 'info'}));

            if (this.model.isBroken)
                return this.$el.html (this.messageTemplate ({message: 'No such job', type: 'danger'}));

            if (this.model.id == "")
                return this.$el.html ('');

            console.log (this.model);
            this.$el.html (this.jobTemplate (this.model.toJSON ()));

            return this;
        },

        onChange: function () {
            this.render();
            return this;
        },

        collapsibleClicked: function (e) {
            $(e.currentTarget).next().toggleClass ('collapsible-closed');
        },

        runScript: function (ev) {
            var script_id = $(ev.currentTarget).data ('script-id');
            var job_id = this.model.id;
            $('#script_'.concat (script_id).concat (' .command .source')).addClass ('queued');
            $('#script_'.concat (script_id).concat (' .stdout-stderr pre')).html('');
            app.appSocket.sendRunScriptRequest (job_id, script_id);
        },

        //createTodoOnEnter: function(e){
        //    if ( e.which !== 13 || !this.input.val().trim() ) { // ENTER_KEY = 13
        //        return;
        //    }
        //    app.todoList.create(this.newAttributes());
        //    this.input.val(''); // clean input box
        //},
        //addOne: function(todo){
        //    var view = new app.TodoView({model: todo});
        //    $('#todo-list').append(view.render().el);
        //},
        //addAll: function(){
        //    this.$('#todo-list').html(''); // clean the todo list
        //    // filter todo item list
        //    switch(window.filter){
        //        case 'pending':
        //            _.each(app.todoList.remaining(), this.addOne);
        //            break;
        //        case 'completed':
        //            _.each(app.todoList.completed(), this.addOne);
        //            break;
        //        default:
        //            app.todoList.each(this.addOne, this);
        //            break;
        //    }
        //},
        //newAttributes: function(){
        //    return {
        //        title: this.input.val().trim(),
        //        completed: false
        //    }
        //}
    });
}) (jQuery);