# encoding: utf-8
# author:   Jan Hybs

import transaction

from flask_wtf import Form
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, EqualTo

from pyrest import db
from pyrest.database.sets.user import User


class SignUpForm (Form):
    username = StringField ('Username', validators=[DataRequired ()])
    password = PasswordField ('Password', validators=[DataRequired ()])
    password_confirm = PasswordField ('Password confirm', validators=[
        DataRequired (),
        EqualTo ('password', message='Passwords must match')
    ])

    def validate (self):
        result = super (Form, self).validate ()
        if not result:
            return result

        user = User.create_user ()
        user.username = self.username.data
        user.password = self.password.data

        print db.users.search_one ({ 'username': self.username.data })
        if db.users.search_one ({ 'username': self.username.data }) is not None:
            self.username.errors.append ('User already exists')
            return False

        db.users.add (user)
        transaction.commit ()

        return True


