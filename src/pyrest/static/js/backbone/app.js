var app = app || {};

$ (function () {
    'use strict';


    //$.ajax('http://localhost/jsapp/data/job-1.json', function ())
    //console.log (app.ScriptCollection.url)

    app.job = new app.Job ();
    app.jobView = new app.JobView ({model: app.job})

    app.router = new app.AppRouter();
    Backbone.history.start();



});