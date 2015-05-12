# encoding: utf-8
# author:   Jan Hybs
from flask_login import current_user
from flask_socketio import emit
import time
import transaction

from pyrest import app, socket, auth, database, authenticated_only, db
from flask import redirect
import subprocess


@socket.on ('connect')
def socket_connect ():
    socket.emit ('debug', 'connected')


@socket.on ('disconnect')
def socket_disconnect ():
    socket.emit ('debug', 'disconnected')


@socket.on ('run-code')
# @authenticated_only
def socket_run_code_request (info):
    # emit ('debug', 'socket_run_code_request for "%"' % current_user.user.username)

    job = db.jobs.get (info['job_id'])
    script = db.scripts.get (info['script_id'])

    details = { 'job_id': info['job_id'], 'script_id': info['script_id'] }

    for command in script.commands:
        # skip empty commands
        if command.is_valid ():

            start_details = details.copy ()
            start_details.update ({ 'command_id': command.id })
            socket.emit ('command-start', start_details)

            process = subprocess.Popen (command.get_source (), shell=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
            for line in iter (process.stdout.readline, ''):
                stdout_details = start_details.copy ()
                stdout_details.update ({ 'stdout': line })
                socket.emit ('stdout', stdout_details)

            for line in iter (process.stderr.readline, ''):
                stderr_details = start_details.copy ()
                stderr_details.update ({ 'stderr': line })
                socket.emit ('stderr', stderr_details)
                # time.sleep(.3)

            end_details = start_details.copy ()
            socket.emit ('command-end', end_details)

                # emit ('debug', message);

                # emit ('city', { 'city': escape (current_user.username + ": " + message['city']) })
                # city = message['city']
                #
                # conference = db.conference.get (city)
                #
                # if conference is None:
                # print 'creating new conference'
                # new_conference = Conference ()
                # new_conference.city = city
                # new_conference.users.append (current_user.username)
                #     # commit changes
                #     db.conference.insert (city, new_conference)
                #     transaction.commit ()
                # else:
                #     print 'updating conference'
                #     conference.users.append (current_user.username)
                #     # commit changes
                #     transaction.commit ()
                #
                # for c in db.conference.items ():
                #     msg = c[1].get_info ()
                #     emit ('city', { 'city': msg })