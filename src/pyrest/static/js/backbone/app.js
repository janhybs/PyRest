var app = app || {};

$ (function () {
    'use strict';


    //$.ajax('http://localhost/jsapp/data/job-1.json', function ())
    //console.log (app.ScriptCollection.url)


    // kick things off by creating the `App`
    app.appView = new app.AppView();
    Backbone.history.start();
});