import transaction, sys
from pyrest import app, socket, auth, db
from pyrest.database.sets.command import CommandManagementApplication
from pyrest.database.sets.job import JobManagementApplication
from pyrest.database.sets.script import ScriptManagementApplication
from pyrest.database.sets.user import UserManagementApplication
from pyrest.server.configuration import Configuration
from gevent import monkey

# register roots for non-existing roots
UserManagementApplication.register (db, 'users', UserManagementApplication)
CommandManagementApplication.register (db, 'commands', CommandManagementApplication)
ScriptManagementApplication.register (db, 'scripts', ScriptManagementApplication)
JobManagementApplication.register (db, 'jobs', JobManagementApplication)

# confirm changes
transaction.commit ()

# set debug Flag if set
app.debug = Configuration.get_instance ().debug

# check arguments and run server is desired
if not Configuration.get_instance ().noserver:
    # run server
    monkey.patch_all(thread=False)
    socket.run (app, host='0.0.0.0', port=5000)
