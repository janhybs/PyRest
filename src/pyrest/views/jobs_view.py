# encoding: utf-8
# author:   Jan Hybs
from flask.templating import render_template
import time

from pyrest import app, socket, auth, database, templated, with_tittle, authenticated_only, db, json_response, _jobs_, _api_
from flask import redirect, Blueprint, flash, url_for, g, request, jsonify, Response
from pyrest.forms.create_job_form import JobForm



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
    time.sleep (.165)
    # job_id = db.jobs.search_one ().id
    job = db.jobs.get (job_id) if job_id else None

    if not job:
        return Response("no such job", status=404)

    return job.as_dict (peek=False)


@_api_.route ('/jobs')
@json_response
def api_get_jobs ():
    time.sleep (0.15)
    jobs = db.jobs.search (sort="name")
    joblist = [job.as_dict (peek=True) for job in jobs]
    return joblist


@_jobs_.route ("/delete")
def sign_out ():
    return 'Foo'