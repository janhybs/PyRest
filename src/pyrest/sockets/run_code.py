# encoding: utf-8
# author:   Jan Hybs
import time
import transaction

from pyrest import app, socket, auth, database, db
from pyrest.database.sets.script import ScriptExitCode
from pyrest.server.dotdict import DotDict
from pyrest.server.flask_utils import emit_event
from pyrest.sockets.async import AsyncProcess
from pyrest.utils.utils import millis


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

    script = db.scripts.get (info.script_id)
    rerun = script.exit_code != ScriptExitCode.unknown

    # prepare base event
    base_event = DotDict ()
    base_event.script_id = info.script_id

    worst_exit_code = 0

    # emit script start event
    script_start = base_event.copy ()
    script_start.start_at = millis ()
    emit_event ('script-start', script_start);
    # update script start timestamp
    script.start_at = script_start.start_at

    for command in script.commands:

        # prepare command event base
        command_event = base_event.copy ()
        command_event.command_id = command.id

        # emit command start event
        command_start = command_event.copy ()
        command_start.start_at = millis ()
        emit_event ('command-start', command_start)
        # update command attr
        command.start_at = command_start.start_at


        process = AsyncProcess (command.get_source ())
        (o, e) = process.run ()

        while process.is_running ():
            # get all stdout lines and emit them
            lines = []
            while not o.empty ():
                lines.append ({ 'type': 'stdout', 'line': o.get () })

            if lines:
                # emit script output event
                command_output = command_event.copy ()
                command_output.output = lines
                emit_event ('command-output', command_output)
                # add lines to command list
                command.outputLines.extend (lines)

            # get all stderr lines and emit them
            lines = []
            while not e.empty ():
                lines.append ({ 'type': 'stderr', 'line': e.get () })

            if lines:
                # emit script output event
                command_output = command_event.copy ()
                command_output.output = lines
                emit_event ('command-output', command_output)
                # add lines to command list
                command.outputLines.extend (lines)

            time.sleep (0.01)

        exit_code = process.wait ()

        # emit command end event
        command_end = command_start.copy ()
        command_end.exit_code = exit_code
        command_end.duration = millis () - command_end.start_at
        emit_event ('command-end', command_end)
        # update command exit and duration
        command.duration = command_end.duration
        command.exit_code = exit_code

        worst_exit_code = max (worst_exit_code, exit_code)

    # emit script end event
    script_end = script_start.copy ()
    script_end.duration = millis () - script_end.start_at
    script_end.exit_code = worst_exit_code
    emit_event ('script-end', script_end)
    # update script exit and duration
    script.exit_code = script_end.exit_code
    script.duration = script_end.duration

    transaction.commit ()
