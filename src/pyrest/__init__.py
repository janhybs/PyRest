# encoding: utf-8
# author:   Jan Hybs

import functools, ZODB.FileStorage, ZODB.DB
from flask import Flask, request
from flask_login import current_user
from flask_socketio import SocketIO
from pyrest.server.auth import Auth

app = Flask (__name__)
app.config['SECRET_KEY'] = 'secretcacas!'
socket = SocketIO (app)
auth = Auth (app)

# settings
app.debug = True

# database = ZODB.DB ('database.fs')
database = ZODB.DB (None)
db_conn = database.open ()
db = db_conn.root



def authenticated_only (f):
    @functools.wraps (f)
    def wrapped (*args, **kwargs):
        if not current_user.is_authenticated ():
            print 'User not authenticated!'
            request.namespace.disconnect ()
        else:
            return f (*args, **kwargs)

    return wrapped

from pyrest.views import index_view, login_view
from pyrest.sockets import  output_socket


app.register_blueprint (login_view.user, url_prefix='/user')