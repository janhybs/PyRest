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
    """
    :param f:
    :return: Decorator which checks whether is given user authenticated
    if not redirect will occur
    """
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
    """
    Decorator which renders template if no valid response is generated
    :param template: name
    :return:
    """
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
    """
    Decorator which sets global object's g tittle based on given attrs
    :param title:
    :param args_:
    :param kwargs_:
    :return:
    """
    def decorator (f):
        @wraps (f)
        def decorated_function (*args, **kwargs):
            g.title = title.format (*args_, **kwargs_)
            return f (*args, **kwargs)

        return decorated_function

    return decorator



def json_response (f):
    """
    Decorator which expects function return value to be json serializable object
    Decorator will then serialize this object to json format and sends response
    :param f:
    :return:
    """
    @functools.wraps (f)
    def decorated_function (*args, **kwargs):
        result = f (*args, **kwargs)
        if isinstance (result, Response):
            return result
        return Response (json.dumps (result, indent=2), mimetype='application/json')

    return decorated_function

#
# injectors
#


@app.context_processor
def inject_request_path_comparison ():
    """
    Injects method for comparing current location
    :return:
    """
    def match_location (id):
        return request.path == url_for (id)

    return dict (match_location=match_location)


@app.context_processor
def inject_get_title ():
    """
    Injects method for getting tittle from g object
    :return:
    """
    def get_title ():
        return g.get ('title', 'Python REST')

    return dict (get_title=get_title)


@app.context_processor
def inject_preview_str ():
    """
    Injects method for shortening string if too long
    :return:
    """
    def str_preview (string, max=32):
        return string if len (string) <= max else string[0:max] + '...'

    return dict (str_preview=str_preview)



@app.context_processor
def inject_pretty_date ():
    """
    Injects method for pretty date formatting
    :return:
    """
    return dict (pretty_date=pretty_date)


#
# other
#


def emit_event (event, data, delay=0):
    """
    Emits socket
    :param event:
    :param data:
    :param delay:
    :return:
    """
    emit (event, data)
    if delay:
        time.sleep (delay)