from flask import Flask, render_template, escape, redirect

from flask_socketio import SocketIO, emit
from flask_login import current_user
import ZODB
import ZODB.FileStorage
import transaction
from database.conference import Conference, ConferenceManagementApplication

from server.auth import Auth, authenticated_only


class G (object):
    # server specific
    server = None
    socket = None
    auth = None

    # database specific
    db_locked = False
    database = None
    db_root = None
    db_storage = None
    db_conn = None


G.server = Flask (__name__)
G.server.config['SECRET_KEY'] = 'secretcacas!'
G.socket = SocketIO (G.server)
G.auth = Auth (G.server)


@G.server.route ("/login/<username>")
def login (username):
    user = G.auth.login (username)
    if user is None:
        return "wrong credentials"

    G.auth.login_user (user)

    print 'login user ' + user.username
    print 'login id' + user.id
    return redirect ('/')


@G.server.route ('/')
def main ():
    return render_template ('main.html')


@G.server.route ("/logout")
def logout ():
    G.auth.logout_user ()
    return redirect ('/')


@G.socket.on ('connect')
def ws_conn ():
    G.socket.emit ('msg', 'co co')


@G.socket.on ('disconnect')
def ws_disconn ():
    G.socket.emit ('msg', 'disco')


@G.socket.on ('city')
@authenticated_only
def ws_city (message):
    # emit ('city', { 'city': escape (current_user.username + ": " + message['city']) })
    city = message['city']

    conference = G.db_root.conference.get (city)

    if conference is None:
        print 'creating new conference'
        new_conference = Conference ()
        new_conference.city = city
        new_conference.users.append (current_user.username)
        # commit changes
        G.db_root.conference.insert (city, new_conference)
        transaction.commit ()
    else:
        print 'updating conference'
        conference.users.append (current_user.username)
        # commit changes
        transaction.commit ()

    for c in G.db_root.conference.items ():
        msg = c[1].get_info ()
        emit ('city', { 'city': msg })


def init_db ():
    try:
        G.db_storage = ZODB.FileStorage.FileStorage ('database.fs')
        G.database = ZODB.DB (G.db_storage)
        G.db_conn = G.database.open ()
        G.db_root = G.db_conn.root

        if not hasattr (G.db_root, 'conference'):
            print 'no conference root, creating'
            G.db_root.conference = ConferenceManagementApplication ()

        transaction.commit ()

    except:
        pass


def init_server ():
    # G.server.debug = True
    G.socket.run (G.server, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    init_db ()
    init_server ()

