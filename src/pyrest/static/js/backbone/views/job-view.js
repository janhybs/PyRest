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
        },
        events: {
            'click .collapsible-command': 'collapsibleClicked'
        },

        render: function () {

            console.log ('rendering job...');

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
            console.log ('model changed');
            this.render();
            return this;
        },

        collapsibleClicked: function (e) {
            $(e.currentTarget).next().toggleClass ('collapsible-closed');
        },
        //events: {
        //    'keypress #new-todo': 'createTodoOnEnter'
        //},
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