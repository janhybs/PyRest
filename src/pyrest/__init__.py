# encoding: utf-8
# author:   Jan Hybs

import functools, ZODB.FileStorage, ZODB.DB
from flask import Flask, request, render_template, url_for, g, redirect
from flask_login import current_user
from flask_socketio import SocketIO

from pyrest.server.auth import Auth
from pyrest.server.configuration import Configuration

app = Flask (__name__)
app.config['SECRET_KEY'] = 'secretcacas!'
socket = SocketIO (app)
auth = Auth (app)


# init memory or file storage
if Configuration.get_instance ().memorystorage:
    database = ZODB.DB (None)
else:
    database = ZODB.DB ('database.fs')

db_conn = database.open ()
db = db_conn.root


def authenticated_only (f):
    @functools.wraps (f)
    def wrapped (*args, **kwargs):
        if not current_user.is_authenticated ():
            print 'User not authenticated!'
            # request.namespace.disconnect ()
            return redirect (url_for ('user.sign_in', redirect_url=request.endpoint))
        else:
            return f (*args, **kwargs)

    return wrapped


from functools import wraps
from flask import request


def templated (template=None):
    def decorator (f):
        @wraps (f)
        def decorated_function (*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint.replace ('.', '/') + '.html'
            ctx = f (*args, **kwargs)
            if ctx is None:
                ctx = { }
            elif not isinstance (ctx, dict):
                return ctx
            return render_template (template_name, **ctx)

        return decorated_function

    return decorator


@app.context_processor
def inject_request_path_comparison ():
    def match_location (id):
        return request.path == url_for (id)

    return dict (match_location=match_location)


@app.context_processor
def inject_get_title ():
    def get_title ():
        return g.get ('title', 'Python REST')

    return dict (get_title=get_title)


@app.context_processor
def inject_preview_str ():
    def str_preview (string, max=32):
        return string if len (string) <= max else string[0:max] + '...'

    return dict (str_preview=str_preview)


def with_tittle (title, *args_, **kwargs_):
    def decorator (f):
        @wraps (f)
        def decorated_function (*args, **kwargs):
            g.title = title.format (*args_, **kwargs_)
            return f (*args, **kwargs)

        return decorated_function

    return decorator


from pyrest.views import index_view, user_view, jobs_view

from pyrest.sockets import output_socket


app.register_blueprint (user_view.user, url_prefix='/user')
app.register_blueprint (jobs_view.jobs, url_prefix='/jobs')