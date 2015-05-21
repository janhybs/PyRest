# encoding: utf-8
# author:   Jan Hybs

import transaction

from flask_wtf import Form
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, EqualTo, Email

from pyrest import db
from pyrest.database.crypto import password_hash
from pyrest.database.sets.user import User, UserManagementApplication


class SignUpForm (Form):
    """
    Form for registration
    """
    username = StringField ('Username', validators=[DataRequired ()])
    password = PasswordField ('Password', validators=[DataRequired ()])
    password_confirm = PasswordField ('Password confirm', validators=[
        DataRequired (),
        EqualTo ('password', message='Passwords must match')
    ])

    email = StringField ('Email', validators=[Email ()])

    def validate (self):
        result = super (Form, self).validate ()
        if not result:
            return result

        if db.users.search_one ({ 'username': self.username.data }) is not None:
            self.username.errors.append ('User already exists')
            return False

        user = UserManagementApplication.create()
        user.username = self.username.data
        user.password = password_hash (self.password.data)

        db.users.add (user)
        transaction.commit ()

        return True


