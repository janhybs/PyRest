# encoding: utf-8
# author:   Jan Hybs
import cgi
from flask.templating import render_template
from werkzeug.datastructures import ImmutableMultiDict

from pyrest import app, socket, auth, database, templated, with_tittle, authenticated_only, db
from flask import redirect, Blueprint, flash, url_for, g, request, jsonify
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
    #     for (key, job_id) in request.form.items (multi=True):
    #         if key == 'job_id':
    #             print db.jobs.get (job_id)

    jobs = db.jobs.search ()
    return render_template ('list_jobs.html', jobs=jobs)


@app.route('/api/jobs/get/<job_id>')
def get_job_by_id (job_id):
    job_id = db.jobs.search_one ().id
    job = db.jobs.get (job_id) if job_id else None
    
    if not job:
        return jsonify({'error': 'no-result'})

    return  jsonify (job.as_dict())


@jobs.route ("/delete")
def sign_out ():
    return 'Foo'