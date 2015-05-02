import transaction, sys
from pyrest import app, socket, auth, db
from pyrest.database.sets.command import CommandManagementApplication
from pyrest.database.sets.job import JobManagementApplication
from pyrest.database.sets.script import ScriptManagementApplication
from pyrest.database.sets.user import UserManagementApplication

# register roots for non-existing roots
UserManagementApplication.register (db, 'users', UserManagementApplication)
JobManagementApplication.register (db, 'jobs', JobManagementApplication)
ScriptManagementApplication.register (db, 'scripts', ScriptManagementApplication)
CommandManagementApplication.register (db, 'commands', CommandManagementApplication)

# confirm changes
transaction.commit ()

#
# print db.users.search_one ({'username': 'Hans', 'password': 'foo'})
# print db.users.search_one ({})


if '--noserver' not in sys.argv:
    # run server
    socket.run (app, host='0.0.0.0', port=5000)
