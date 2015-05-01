import transaction
from pyrest import app, socket, auth, db
from pyrest.database.conference import ConferenceManagementApplication


# create 'root' for conference objects
if not hasattr (db, 'conference'):
    print 'no conference root, creating'
    db.conference = ConferenceManagementApplication ()
    transaction.commit ()

socket.run (app, host='0.0.0.0', port=5000)