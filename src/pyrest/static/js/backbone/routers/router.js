var app = app || {};

$ (function () {
    'use strict';


    app.AppRouter = Backbone.Router.extend({

        routes: {
            "job/:job_id":  "loadJob",
        },

        loadJob: function(job_id, page) {
            app.job.set('id', job_id)
            app.job.fetch ();
        }

    });


});
