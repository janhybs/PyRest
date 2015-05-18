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


        /**
         * Add listeners and clears children
         */
        initialize: function () {
            this.scriptViews = [];
            this.model.on ('change', this.render, this);
            this.listenTo (this.model.scripts, 'reset', this.onCollectionChange);
            this.listenTo (this.model.scripts, 'change', this.onCollectionChange);
        },


        /**
         * Method which destroys whole view and its children if any
         */
        destroy: function () {
            this.remove ();
            this.destroyChildren ();
        },

        /**
         * Method which destroys views children if any
         */
        destroyChildren: function () {
            _.each (this.scriptViews, function (view) {
                view.destroy ();
            });
            this.scriptViews = [];
        },

        /**
         * If collection has changed redraw all views
         */
        onCollectionChange: function () {
            _.each (this.scriptViews, function (view) {
                view.render ();
            })
        },

        /**
         * Method for rendering this view
         * Also draws all scripts when called
         * @returns {app.JobView}
         */
        render: function () {
            this.$el.html (this.jobTemplate (this.model.toJSON ()));
            this.$scripts = this.$ ('.job-scripts');

            this.addAll ();

            // todo more specific listener
            if (this.model.isLoading)
                this.$el.addClass ('disabled');
            else
                this.$el.removeClass ('disabled');

            return this;
        },


        /**
         * Method for rendering one ScriptView
         * @param script
         */
        addOne: function (script) {
            var view = new app.ScriptView ({model: script});
            this.scriptViews.push (view);
            this.$scripts.append (view.render ().el);
        },

        /**
         * Method for rendering all ScriptViews
         */
        addAll: function () {
            this.destroyChildren ();
            this.$scripts.html ('');
            this.model.scripts.each (this.addOne, this);
        }
    });
}) (jQuery);