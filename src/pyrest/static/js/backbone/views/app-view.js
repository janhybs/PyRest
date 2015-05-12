var app = app || {};

(function ($) {
	'use strict';

	// The Application
	// ---------------

	// Our overall **AppView** is the top-level piece of UI.
	app.AppView = Backbone.View.extend({

		// Instead of generating a new element, bind to the existing skeleton of
		// the App already present in the HTML.
		el: '#job-list',
		current_id: '',

		noJobsTemplate: _.template($('#no-jobs-template').html()),

		// Delegated events for creating new items, and clearing completed ones.
		events: {
//			'keypress #new-todo': 'createOnEnter',
//			'click #clear-completed': 'clearCompleted',
//            'click .run-script': 'runScript'
		},

        updateStyles: function (current_id) {
            debug ('updating styles');
            this.current_id = current_id;

            $(".job-link").removeClass('selected');
            $(".job-link[data-job-id='" + this.current_id + "']").addClass('selected');
        },

		// At initialization we bind to the relevant events on the `Todos`
		// collection, when items are added or changed. Kick things off by
		// loading any preexisting todos that might be saved in *localStorage*.
		initialize: function () {
		    debug ('init app view')

		    var that = this;
//			this.allCheckbox = this.$('#toggle-all')[0];
//			this.$input = this.$('#new-todo');
//			this.$footer = this.$('#footer');
//			this.$main = this.$('#main');
			this.$list = $('#job-list');
//
			this.listenTo(app.jobs, 'add', this.addOne);
			this.listenTo(app.jobs, 'reset', this.addAll);
			this.listenTo(app.appRouter, 'jobIdChange', this.onJobIdChange);
//			this.listenTo(app.todos, 'change:completed', this.filterOne);
//			this.listenTo(app.todos, 'filter', this.filterAll);
//			this.listenTo(app.todos, 'all', _.debounce(this.render, 0));

			// Suppresses 'add' events with {reset: true} and prevents the app view
			// from being re-rendered for every model. Only renders when the 'reset'
			// event is triggered at the end of the fetch.

            debug ('fetching job-list...')
			app.jobs.fetch({reset: true,
			    success: function() {
                    debug ('fetch job-list ok')
			        // check jobs obtained
			        if (app.jobs.length == 0) {
			            // no jobs found, create one
			            that.render ();
			            return;
			        }

			        // check current url
			        if (app.appRouter.job_id === false) {
			            // on empty route, set id of first received job_id
			            var job_id = app.jobs.models[0].id;
			            app.appRouter.navigate ('job/'+job_id, {trigger: true});
			        } else {
			            // trigger job id change after render is complete
			            app.appRouter.trigger ('jobIdChange', app.appRouter.job_id);
			        }
			    }
			});
		},

        onJobIdChange: function (job_id) {
            debug ('onJobIdChange ' + job_id);
            this.updateStyles (job_id);
        },

		// Re-rendering the App just means refreshing the statistics -- the rest
		// of the app doesn't change.
		render: function () {
		    debug ('render app');
		    if (app.jobs.length == 0) {
		        this.$el.html (this.noJobsTemplate ({  }));
		        app.jobView.render ();
		    }
//			var completed = app.todos.completed().length;
//			var remaining = app.todos.remaining().length;
//
//			if (app.todos.length) {
//				this.$main.show();
//				this.$footer.show();
//
//				this.$footer.html(this.statsTemplate({
//					completed: completed,
//					remaining: remaining
//				}));
//
//				this.$('#filters li a')
//					.removeClass('selected')
//					.filter('[href="#/' + (app.TodoFilter || '') + '"]')
//					.addClass('selected');
//			} else {
//				this.$main.hide();
//				this.$footer.hide();
//			}
//
//			this.allCheckbox.checked = !remaining;
		},

		addOne: function (job) {
			var view = new app.JobPeekView({ model: job });
			this.$list.append(view.render().el);
		},

		// Add all items in the **Todos** collection at once.
		addAll: function () {
		    debug ('adding jobs')
			this.$list.html('');
			app.jobs.each(this.addOne, this);
		},

//		filterOne: function (tovdo) {
//			tovdo.trigger('visible');
//		},
//
//		filterAll: function () {
//			app.jobs.each(this.filterOne, this);
//		},

		// Generate the attributes for a new Tovdo item.
//		newAttributes: function () {
//			return {
//				title: this.$input.val().trim(),
//				order: app.todos.nextOrder(),
//				completed: false
//			};
//		},
	});

    app.job = new app.Job ();
    app.jobView = new app.JobView ({model: app.job})
})(jQuery);