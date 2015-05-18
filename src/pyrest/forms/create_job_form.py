# encoding: utf-8
# author:   Jan Hybs
from flask_login import current_user

import transaction

from flask_wtf import Form
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email

from pyrest import db
from pyrest.database.sets.job import JobManagementApplication
from pyrest.database.sets.script import ScriptManagementApplication
from pyrest.database.sets.user import User


class JobForm (Form):
    """
    Form for creating new Job
    """
    name = StringField ('name', validators=[DataRequired ()])
    script = TextAreaField ('script', validators=[DataRequired ()])

    def validate (self):
        result = super (Form, self).validate ()
        if not result:
            return result

        if db.jobs.search_one ({ 'name': self.name.data }) is not None:
            self.username.errors.append ('Job with this name already exists')
            return False

        # create job instance and default script instance
        job = JobManagementApplication.create (user_id=current_user.user.id, name=self.name.data)
        script = ScriptManagementApplication.create (job_id=job.id, commands=self.script.data)

        # add default instance id to jobs scripts list
        job.add_script (script)

        # add script and job to db
        db.scripts.add (script)
        db.jobs.add (job)

        #commit changes
        transaction.commit ()

        return True


