var app = {}; // create namespace for our app

app.Todo = Backbone.Model.extend ({
    defaults: {
        title: '',
        completed: false
    },
    toggle: function () {
        this.save ({completed: !this.get ('completed')});
    }
});

app.TodoList = Backbone.Collection.extend ({
    model: app.Todo,
    localStorage: new Store ("backbone-todo")
});

app.todoList = new app.TodoList ();

// renders individual two-doo items list (li)
app.TodoView = Backbone.View.extend ({
    tagName: 'li',
    template: _.template ($ ('#item-template').html ()),
    render: function () {
        console.log ('rendering');
        this.$el.html (this.template (this.model.toJSON ()));
        this.input = this.$ ('.edit');
        return this; // enable chained calls
    },
    initialize: function () {
        this.model.on ('change', this.render, this);
        this.model.on ('destroy', this.remove, this); // remove: Convenience Backbone'
    },
    events: {
        'dblclick label': 'edit',
        'keypress .edit': 'updateOnEnter',
        'blur .edit': 'close',
        'click .toggle': 'toggleCompleted',
        'click .destroy': 'destroy'
    },
    destroy: function (e) {
        this.model.destroy ();
    },
    edit: function () {
        this.$el.addClass ('editing');
        this.input.focus ();
    },
    close: function () {
        var value = this.input.val ().trim ();
        console.log (this.model.get ('title'));
        console.log (value);
        if (value) {
            this.model.save ({title: value});
        }
        this.$el.removeClass ('editing');
    },
    updateOnEnter: function (e) {
        if (e.which == 13) {
            this.close ();
        }
    },
    toggleCompleted: function () {
        this.model.toggle ();
    }
});


// renders the full list of two-doo items calling TodoView for each one.
app.AppView = Backbone.View.extend ({
    el: '#todoapp',
    initialize: function () {
        this.input = this.$ ('#new-todo');
        // when new elements are added to the collection render then with addOne
        app.todoList.on ('add', this.addOne, this);
        app.todoList.on ('reset', this.addAll, this);
        app.todoList.on ('remove', this.removeModel, this);
        app.todoList.fetch (); // Loads list from local storage
    },
    events: {
        'keypress #new-todo': 'createTodoOnEnter'
    },
    removeModel: function (e) {
        console.log ('remove');
        console.log (e);
    },
    createTodoOnEnter: function (e) {
        if (e.which !== 13 || !this.input.val ().trim ()) { // ENTER_KEY = 13
            return;
        }
        app.todoList.create (this.newAttributes ());
        this.input.val (''); // clean input box
    },
    addOne: function (todo) {
        console.log ('add');
        var view = new app.TodoView ({model: todo});
        $ ('#todo-list').append (view.render ().el);
    },
    addAll: function () {
        console.log ('reset');
        this.$ ('#todo-list').html (''); // clean the two-doo list
        app.todoList.each (this.addOne, this);
    },
    newAttributes: function () {
        return {
            title: this.input.val ().trim (),
            completed: false
        }
    }
});


var AppRouter = Backbone.Router.extend ({
    routes: {
        "test/:id": "getId", // matches http://example.com/#test/anything-here accessable as id
        "*actions": "defaultRoute" // matches http://example.com/#anything-here
    }
});
app.router = new AppRouter ();

app.router.on ('route:getId', function (actions) {
    console.log ('getId');
    console.log (actions);
});

app.router.on ('route:defaultRoute', function (actions) {
    console.log ('defaultRoute');
    console.log (actions);
});

Backbone.history.start ();

//--------------
// Initializers
//--------------

app.appView = new app.AppView ();
