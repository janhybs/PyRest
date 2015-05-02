# encoding: utf-8
# author:   Jan Hybs

from flask_wtf import Form
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, EqualTo
from pyrest import db, auth


class SignUpForm (Form):
    username = StringField ('Username', validators=[DataRequired ()])
    password = PasswordField ('Password', validators=[DataRequired ()])
    password_confirm = PasswordField ('Password confirm', validators=[
        DataRequired (),
        EqualTo ('Password', message='Passwords must match')
    ])

    def validate (self):
        result = super (Form, self).validate ()
        if not result:
            return result

        user = db.users.search_one ({ 'username': self.username.data, 'password': self.password.data })
        print user
        if user is not None:
            auth.login_user (user.create_session_user ())

        return True

