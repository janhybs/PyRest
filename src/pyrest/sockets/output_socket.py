# encoding: utf-8
# author:   Jan Hybs
from flask_login import current_user
from flask_socketio import emit
import transaction

from pyrest import app, socket, auth, database, authenticated_only, db
from flask import redirect


@socket.on ('connect')
def socket_connect ():
    socket.emit ('debug', 'connected')


@socket.on ('disconnect')
def logout ():
    socket.emit ('debug', 'disconnected')


@socket.on ('city')
@authenticated_only
def ws_city (message):
    # emit ('city', { 'city': escape (current_user.username + ": " + message['city']) })
    city = message['city']

    conference = db.conference.get (city)

    if conference is None:
        print 'creating new conference'
        new_conference = Conference ()
        new_conference.city = city
        new_conference.users.append (current_user.username)
        # commit changes
        db.conference.insert (city, new_conference)
        transaction.commit ()
    else:
        print 'updating conference'
        conference.users.append (current_user.username)
        # commit changes
        transaction.commit ()

    for c in db.conference.items ():
        msg = c[1].get_info ()
        emit ('city', { 'city': msg })