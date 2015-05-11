/*global Backbone, jQuery, _, ENTER_KEY */
var app = app || {};

(function ($) {
    'use strict';

    // The Application
    // ---------------

    app.JobPeekView = Backbone.View.extend ({
        // list tag
        tagName: 'li',

        jobTemplate: _.template ($ ('#job-peek-template').html ()),

        initialize: function () {
            this.model.on ('change', this.render, this);
            this.render ();
        },
        events: {
//            'click .collapsible-command': 'collapsibleClicked'
        },

        render: function () {
            this.$el.html (this.jobTemplate (this.model.toJSON ()));
            return this;
        }
    });
}) (jQuery);
