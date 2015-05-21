# encoding: utf-8
# author:   Jan Hybs
from flask.templating import render_template
import time

from pyrest import app, socket, auth, database,  db, _jobs_
from flask import redirect, Blueprint, flash, url_for, g, request, jsonify, Response
from pyrest.database.sets.command import CommandManagementApplication
from pyrest.forms.create_job_form import JobForm
from pyrest.database.sets.script import ScriptExitCode, ScriptManagementApplication
from pyrest.server.flask_utils import authenticated_only, json_response
from pyrest.server.flask_utils import with_tittle


@_jobs_.route ("/new", methods=['GET', 'POST'])
@with_tittle ('New job')
@authenticated_only
def create_job ():
    """
    form handler for creating new job
    """
    form = JobForm ()
    if form.validate_on_submit ():
        flash (u'Job successfully created', category='success')
        return redirect (url_for ('jobs.list_jobs'))
    return render_template ('create_job_form.html', form=form)


@_jobs_.route ("/list")
@authenticated_only
def list_jobs ():
    """
    shows page with all jobs created by current user
    """
    return render_template ('list_jobs.html')