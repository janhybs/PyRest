# encoding: utf-8
# author:   Jan Hybs
from flask_login import current_user
from flask_socketio import emit
import time
import transaction

from pyrest import app, socket, auth, database, authenticated_only, db, millis, emit_event
from flask import redirect
import subprocess
from pyrest.database.sets.script import ScriptExitCode
from pyrest.server.dotdict import DotDict
from pyrest.sockets.async import AsyncProcess


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

    info = DotDict (info)

    job = db.jobs.get (info.job_id)
    script = db.scripts.get (info.script_id)
    rerun = script.exit_code != ScriptExitCode.unknown

    base_event = DotDict ()
    base_event.job_id = info.job_id
    base_event.script_id = info.script_id

    script.start_at = millis ()
    worst_exit_code = 0

    for command in script.commands:

        command_event = base_event.copy ()
        command_event.command_id = command.id

        event_start = command_event.copy ()
        event_start.start_at = millis ()
        emit_event ('command-start', event_start)
        command.start_at = event_start.start_at

        process = AsyncProcess (command.get_source ())
        (o, e) = process.run ()

        while process.is_running ():
            # get all stdout lines and emit them
            lines = []
            while not o.empty ():
                lines.append ({ 'type': 'stdout', 'line': o.get () })

            if lines:
                output_event = command_event.copy ()
                output_event.output = lines
                emit_event ('command-output', output_event)
                command.outputLines.extend (lines)

            # get all stderr lines and emit them
            lines = []
            while not e.empty ():
                lines.append ({ 'type': 'stderr', 'line': e.get () })

            if lines:
                output_event = command_event.copy ()
                output_event.output = lines
                emit_event ('command-output', output_event)
                command.outputLines.extend (lines)

            time.sleep (0.3)

        exit_code = process.wait ()

        event_end = event_start.copy ()
        event_end.exit_code = exit_code
        event_end.duration = millis () - event_end.start_at
        emit_event ('command-end', event_end)

        command.duration = event_end.duration
        command.exit_code = exit_code

        worst_exit_code = max (worst_exit_code, exit_code)

    script.exit_code = worst_exit_code
    script.duration = millis () - script.start_at
    transaction.commit ()
