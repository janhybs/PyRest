/*global Backbone, jQuery, _, ENTER_KEY */
var app = app || {};

(function ($) {
    'use strict';

    // The Application
    // ---------------

    // renders the full list of todo items calling TodoView for each one.
    app.CommandView = Backbone.View.extend ({
        tagName: 'div',

        jobTemplate: _.template ($ ('#command-template').html ()),
        messageTemplate: _.template ($ ('#message-template').html ()),


        initialize: function () {
            this.model.on ('change', this.onChange, this);
        },
        events: {
        },


        render: function () {
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
    });
}) (jQuery);