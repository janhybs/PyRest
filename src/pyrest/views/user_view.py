# encoding: utf-8
# author:   Jan Hybs
from flask.templating import render_template

from pyrest import app, socket, auth, database, templated
from flask import redirect, Blueprint, flash
from pyrest.forms.login_form import LoginForm
from pyrest.forms.sign_up_form import SignUpForm


user = Blueprint ('user', __name__, template_folder='templates')


@user.route ("/login", methods=['GET', 'POST'])
def login ():
    form = LoginForm ()
    if form.validate_on_submit ():
        flash (u'Successfully logged in as %s' % form.username.data)
        return redirect ('/')
    return render_template ('login_form.html', form=form)


@user.route ("/sign-up", methods=['GET', 'POST'])
def sign_up ():
    form = SignUpForm ()
    if form.validate_on_submit ():
        flash (u'Successfully registered as %s' % form.username.data)
        return redirect ('/')
    return render_template ('sign_up_form.html', form=form)


@user.route ("/logout")
def logout ():
    auth.logout_user ()
    return redirect ('/')