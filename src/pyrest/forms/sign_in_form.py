# encoding: utf-8
# author:   Jan Hybs

from flask_wtf import Form
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired
from pyrest import db, auth


class SignInForm (Form):
    """
    Form for login
    """
    username = StringField ('Username', validators=[DataRequired ()])
    password = PasswordField ('Password', validators=[DataRequired ()])

    def validate (self):
        result = super (Form, self).validate ()
        if not result:
            return result

        user = db.users.search_one ({ 'username': self.username.data, 'password': self.password.data })
        if user is not None:
            auth.login_user (user.create_session_user ())
        else:
            self.password.errors.append('Wrong password or username')
            return False

        return True

