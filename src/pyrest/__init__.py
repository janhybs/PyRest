# encoding: utf-8
# author:   Jan Hybs

import ZODB.FileStorage
import ZODB.DB
from flask import Flask, Blueprint
from flask_socketio import SocketIO

from pyrest.server.auth import Auth
from pyrest.server.configuration import Configuration




# create app
app = Flask (__name__)
app.config['SECRET_KEY'] = 'not really secret key'
socket = SocketIO (app)
auth = Auth (app)


# init memory or file storage
if Configuration.get_instance ().memorystorage:
    database = ZODB.DB (None)
else:
    database = ZODB.DB ('database.fs')

# open db
db_conn = database.open ()
db = db_conn.root


# build blueprints
_jobs_ = Blueprint ('jobs', __name__, template_folder='templates')
_user_ = Blueprint ('user', __name__, template_folder='templates')
_api_ = Blueprint ('api', __name__, template_folder='templates')

# import views
from pyrest.views import index_view, user_view, jobs_view
from pyrest.sockets import run_code
from pyrest.rest.jobs_api import JobsApi
from pyrest.rest.scripts_api import ScriptsApi

# register blueprints
app.register_blueprint (_user_, url_prefix='/user')
app.register_blueprint (_jobs_, url_prefix='/jobs')
# app.register_blueprint (_api_, url_prefix='/api')
JobsApi.register(app, route_base='/api/jobs/')
ScriptsApi.register(app, route_base='/api/scripts/')