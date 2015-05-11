/*global Backbone */
var app = app || {};

(function () {
	'use strict';

	// Todo Collection
	// ---------------

	app.Jobs = Backbone.Collection.extend({
		model: app.Job,
		url: "/api/jobs",

		comparator: 'name'
	});

	app.jobs = new app.Jobs();
})();