# encoding: utf-8
# author:   Jan Hybs
import json
from flask_login import current_user
from flask import redirect, g, Response
import functools
from flask_socketio import emit
import time
from pyrest import app
from pyrest.utils.utils import pretty_date


#
# decorators
#

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
from flask import request, render_template, url_for


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




def with_tittle (title, *args_, **kwargs_):
    def decorator (f):
        @wraps (f)
        def decorated_function (*args, **kwargs):
            g.title = title.format (*args_, **kwargs_)
            return f (*args, **kwargs)

        return decorated_function

    return decorator


#
# injectors
#


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



@app.context_processor
def inject_pretty_date ():
    return dict (pretty_date=pretty_date)


def json_response (f):
    @functools.wraps (f)
    def decorated_function (*args, **kwargs):
        result = f (*args, **kwargs)
        if isinstance (result, Response):
            return result
        return Response (json.dumps (result, indent=2), mimetype='application/json')

    return decorated_function

#
# other
#


def emit_event (event, data, delay=0):
    # print 'emitting: {} {}'.format (event, str (data))
    emit (event, data)
    if delay:
        time.sleep (delay)