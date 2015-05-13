# encoding: utf-8
# author:   Jan Hybs

import functools, ZODB.FileStorage, ZODB.DB
import json, time
from flask import Flask, request, render_template, url_for, g, redirect, Response, Blueprint
from flask_login import current_user
from flask_socketio import SocketIO
from datetime import datetime

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


def pretty_date (time=False, now_=None):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    now = datetime.now () if now_ is None else now_
    if type (time) is int or type (time) is float:
        diff = now - datetime.fromtimestamp (time)
    elif isinstance (time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str (second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str (second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str (second_diff / 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str (day_diff) + " days ago"
    if day_diff < 31:
        return str (day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return str (day_diff / 30) + " months ago"
    return str (day_diff / 365) + " years ago"


@app.context_processor
def inject_pretty_date ():
    return dict (pretty_date=pretty_date)


def with_tittle (title, *args_, **kwargs_):
    def decorator (f):
        @wraps (f)
        def decorated_function (*args, **kwargs):
            g.title = title.format (*args_, **kwargs_)
            return f (*args, **kwargs)

        return decorated_function

    return decorator


def json_response (f):
    @functools.wraps (f)
    def decorated_function (*args, **kwargs):
        result = f (*args, **kwargs)
        if isinstance (result, Response):
            return result
        return Response (json.dumps (result, indent=2), mimetype='application/json')

    return decorated_function


start_time = time.time ()


def millis (since_start=False):
    dt = time.time () - start_time if since_start else time.time ()
    return int(dt * 1000)

# build blueprints
_jobs_ = Blueprint ('jobs', __name__, template_folder='templates')
_user_ = Blueprint ('user', __name__, template_folder='templates')
_api_ = Blueprint ('api', __name__, template_folder='templates')



# import views
from pyrest.views import index_view, user_view, jobs_view
from pyrest.sockets import run_code

# register blueprints
app.register_blueprint (_user_, url_prefix='/user')
app.register_blueprint (_jobs_, url_prefix='/jobs')
app.register_blueprint (_api_, url_prefix='/api')