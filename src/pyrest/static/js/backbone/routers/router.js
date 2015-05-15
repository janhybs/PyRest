var app = app || {};

$ (function () {
    'use strict';


    app.AppRouter = Backbone.Router.extend({

        noRoute:  true,

        routes: {
            "job/:job_id":  "loadJob",
            "*anoything": "lastHook"
        },

        loadJob: function(job_id, page) {
            this.job_id = job_id;

//            debug ('triggering');
            this.trigger('jobIdChange', this.job_id);

            app.job.id = job_id
            app.job.isLoading = true;
            app.job.isBroken = false;
            app.jobView.render();

            app.job.fetch ({
                success: function () {
                    app.job.isLoading = false;
                    app.job.isBroken = false;
                    app.jobView.render();
                },
                error: function () {
                    app.job.isLoading = false;
                    app.job.isBroken = true;
                    app.jobView.render();
                }
            });
        },

        lastHook: function (page) {
            this.job_id = false;
        }

    });

    app.appRouter = new app.AppRouter();


});
