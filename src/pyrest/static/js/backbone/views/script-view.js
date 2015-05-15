/*global Backbone, jQuery, _, ENTER_KEY */
var app = app || {};

(function ($) {
    'use strict';

    // The Application
    // ---------------

    // renders the full list of todo items calling TodoView for each one.
    app.ScriptView = Backbone.View.extend ({
        tagName: 'li',

        jobTemplate: _.template ($ ('#script-template').html ()),
        messageTemplate: _.template ($ ('#message-template').html ()),


        initialize: function () {
            this.model.on ('change', this.onChange, this);
//            this.model.commands.on ('add', this.addOne);
//			this.model.commands.on ('reset', this.addAll);
        },
        events: {
        },


        render: function () {
            this.$el.html (this.jobTemplate (this.model.toJSON ()));
            this.$commands = this.$el.find('.script-commands');
            window.el = this.$el;

            this.addAll ();
            return this;
        },

        onChange: function () {
            this.render();
            return this;
        },

		addOne: function (command) {
		    if (!command.isValid())
                return this;

			var view = new app.CommandView({ model: command });
			this.$commands.append(view.render().el);
			return this;
		},

		addAll: function () {
		    debug ('adding scripts')
			this.$commands.html('');
			this.model.commands.each(this.addOne, this);
		},
    });
}) (jQuery);