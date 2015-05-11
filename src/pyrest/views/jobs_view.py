# encoding: utf-8
# author:   Jan Hybs
import cgi
import json
from flask.templating import render_template
import time
from werkzeug.datastructures import ImmutableMultiDict

from pyrest import app, socket, auth, database, templated, with_tittle, authenticated_only, db, json_response
from flask import redirect, Blueprint, flash, url_for, g, request, jsonify, Response
from pyrest.forms.create_job_form import JobForm


jobs = Blueprint ('jobs', __name__, template_folder='templates')


@jobs.route ("/new", methods=['GET', 'POST'])
@with_tittle ('New job')
@authenticated_only
def create_job ():
    form = JobForm ()
    if form.validate_on_submit ():
        flash (u'Job successfully created', category='success')
        return redirect (url_for ('main'))
    return render_template ('create_job_form.html', form=form)


@jobs.route ("/list")
def list_jobs ():
    # if request.form:
    # for (key, job_id) in request.form.items (multi=True):
    # if key == 'job_id':
    #             print db.jobs.get (job_id)


    # return jsonify([job.as_dict(peek=True) for job in jobs])
    return render_template ('list_jobs.html', jobs=jobs)


@app.route ('/api/jobs/<job_id>')
@json_response
def api_get_job_by_id (job_id):
    time.sleep (.5)
    # job_id = db.jobs.search_one ().id
    job = db.jobs.get (job_id) if job_id else None

    if not job:
        return Response("no such job", status=404)

    return job.as_dict (peek=False)


@app.route ('/api/jobs')
@json_response
def api_get_jobs ():
    time.sleep (1.0)
    jobs = db.jobs.search (sort="name")
    jobList = [job.as_dict (peek=True) for job in jobs]
    return jobList


@jobs.route ("/delete")
def sign_out ():
    return 'Foo'