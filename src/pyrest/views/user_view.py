# encoding: utf-8
# author:   Jan Hybs

from pyrest import app, socket, auth, database
from flask import redirect, Blueprint


user = Blueprint ('user', __name__, template_folder='templates')


@user.route ("/login/<username>")
def login (username):
    user = auth.login (username)
    if user is None:
        return "wrong credentials"

    auth.login_user (user)

    print 'login user ' + user.username
    print 'login id' + user.id
    return redirect ('/')


@user.route ("/logout")
def logout ():
    auth.logout_user ()
    return redirect ('/')