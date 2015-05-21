# encoding: utf-8
# author:   Jan Hybs
from flask.templating import render_template

from pyrest import app, socket, auth, database, _user_
from flask import redirect, Blueprint, flash, url_for
from pyrest.forms.sign_in_form import SignInForm
from pyrest.forms.sign_up_form import SignUpForm
from pyrest.server.flask_utils import with_tittle


@_user_.route ("/sign-in", methods=['GET', 'POST'], defaults={ 'redirect_url': 'main' })
@_user_.route ("/sign-in/<redirect_url>", methods=['GET', 'POST'])
@with_tittle ('Sign in')
def sign_in (redirect_url):
    """
    form handler for logging
    """
    form = SignInForm ()
    if form.validate_on_submit ():
        flash (u'Successfully logged in as %s' % form.username.data, category='success')
        return redirect (url_for (redirect_url))

    return render_template ('sign_in_form.html', form=form)


@_user_.route ("/sign-up", methods=['GET', 'POST'])
@with_tittle ('Sign up')
def sign_up ():
    """
    form handler for creating new user
    """
    form = SignUpForm ()
    if form.validate_on_submit ():
        flash (u'Successfully registered as %s' % form.username.data, category='success')
        return redirect (url_for ('user.sign_in'))
    return render_template ('sign_up_form.html', form=form)


@_user_.route ("/sign_out")
def sign_out ():
    """
    sign out user
    """
    auth.logout_user ()
    return redirect (url_for ('main'))