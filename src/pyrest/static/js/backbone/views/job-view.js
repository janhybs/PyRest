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
            this.renderAll = true;
            this.scriptViews = [];
            this.model.on ('change', this.render, this);
            this.listenTo (this.model.scripts, 'reset', this.onCollectionChange);
            this.listenTo (this.model.scripts, 'change', this.onCollectionChange);
        },


        destroy: function () {
            this.remove ();
            this.destroyChildren ();
        },

        destroyChildren: function () {
            _.each (this.scriptViews, function (view) {
                view.destroy ();
            });
            this.scriptViews = [];
        },

        onCollectionChange: function () {
            _.each(this.scriptViews, function (view) {
                view.render();
            })
        },

        render: function () {
            this.$el.html (this.jobTemplate (this.model.toJSON ()));
            this.$scripts = this.$ ('.job-scripts');

            this.addAll ();

            if (this.model.isLoading)
                this.$el.addClass ('disabled');
            else
                this.$el.removeClass ('disabled');

            return this;
        },


        addOne: function (script) {
            var view = new app.ScriptView ({model: script});
            this.scriptViews.push(view);
            this.$scripts.append (view.render ().el);
        },

        addAll: function () {
            this.destroyChildren ();
            this.$scripts.html ('');
            this.model.scripts.each (this.addOne, this);
        },
    });
}) (jQuery);