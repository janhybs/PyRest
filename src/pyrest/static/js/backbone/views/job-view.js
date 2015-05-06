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

        initialize: function () {
            this.$loading = this.$ ('.job-loading');
            this.$content = this.$ ('.job-content');

            this.model.on ('change', this.render, this);

            this.render ();
        },

        render: function () {
            this.$el.html (this.jobTemplate (this.model.toJSON ()));
            console.log (this.model.toJSON ());
            return this;
        }
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