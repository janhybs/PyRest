# encoding: utf-8
# author:   Jan Hybs
from flask.templating import render_template
import time

from pyrest import app, socket, auth, database, templated, with_tittle, authenticated_only, db, json_response, _jobs_, \
    _api_
from flask import redirect, Blueprint, flash, url_for, g, request, jsonify, Response
from pyrest.database.sets.command import CommandManagementApplication
from pyrest.forms.create_job_form import JobForm
from pyrest.database.sets.script import ScriptExitCode, ScriptManagementApplication


@_jobs_.route ("/new", methods=['GET', 'POST'])
@with_tittle ('New job')
@authenticated_only
def create_job ():
    form = JobForm ()
    if form.validate_on_submit ():
        flash (u'Job successfully created', category='success')
        return redirect (url_for ('main'))
    return render_template ('create_job_form.html', form=form)


@_jobs_.route ("/list")
def list_jobs ():
    return render_template ('list_jobs.html')


@_api_.route ('/jobs/<job_id>')
@json_response
def api_get_job_by_id (job_id):
    time.sleep(0.5)
    # job_id = db.jobs.search_one ().id
    job = db.jobs.get (job_id) if job_id else None

    if not job:
        return Response ("no such job", status=404)

    return job.as_dict (peek=False)


@_api_.route ('/jobs')
@json_response
def api_get_jobs ():
    time.sleep(0.5)
    jobs = db.jobs.search (sort="name")
    joblist = [job.as_dict (peek=True) for job in jobs]
    return joblist


@_api_.route ('/scripts/<script_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@_api_.route ('/scripts/', methods=['GET', 'POST', 'PUT', 'DELETE'], defaults={ 'script_id': '' })
@json_response
def api_scripts_by_id (script_id):
    time.sleep(0.5)
    script = db.scripts.get (script_id)

    if request.method == 'PUT':
        # remove insides
        if script.exit_code == ScriptExitCode.unknown:
            commands = request.json['commandsNew'].splitlines ()
            script.commands = CommandManagementApplication.create_command_list (script_id=script.id, commands=commands)

            return { 'update': 'ok' }
        else:
            cp = script.copy ()
            commands = request.json['commandsNew'].splitlines ()
            cp.commands = CommandManagementApplication.create_command_list (script_id=script.id, commands=commands)

            return cp.as_dict ()

    if request.method == "POST":
        job_id = request.json['job_id']
        job = db.jobs.get (job_id)
        script = ScriptManagementApplication.create (job_id=job_id, commands=request.json['commandsNew'])
        job.add_script (script)
        db.scripts.add (script)

        return { 'insert': 'ok' }

    if request.method == 'GET':
        return script.as_dict ()

    return Response (status=404);


@_jobs_.route ("/delete")
def sign_out ():
    return 'Foo'