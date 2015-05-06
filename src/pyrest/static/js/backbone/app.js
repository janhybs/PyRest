var app = app || {};

$ (function () {
    'use strict';


    //$.ajax('http://localhost/jsapp/data/job-1.json', function ())
    //console.log (app.ScriptCollection.url)

    var job = new app.Job ({id: 'job-1.json'});
    job.fetch ({
        success: function (model, response) {
            window.job = job;
            new app.JobView ({model: job});
        }
    });


});