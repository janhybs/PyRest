# encoding: utf-8
# author:   Jan Hybs
import cgi
from flask.templating import render_template

from pyrest import app, socket, auth, database, templated, with_tittle, authenticated_only, db
from flask import redirect, Blueprint, flash, url_for, g, request
from pyrest.forms.create_job_form import JobForm


jobs = Blueprint ('jobs', __name__, template_folder='templates')


@jobs.route ("/new", methods=['GET', 'POST'])
@with_tittle('New job')
@authenticated_only
def create_job ():
    form = JobForm ()
    if form.validate_on_submit ():
        flash (u'Job successfully created', category='success')
        return redirect (url_for ('main'))
    return render_template ('create_job_form.html', form=form)


@jobs.route ("/list", methods=['GET', 'POST'])
def list_jobs ():
    print request.form['job_id']
    jobs = db.jobs.search()
    return render_template ('list_jobs.html', jobs=jobs)


@jobs.route ("/delete")
def sign_out ():
    return 'Foo'