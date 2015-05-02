# encoding: utf-8
# author:   Jan Hybs

import functools, uuid
from flask import request, session
from flask_login import LoginManager, UserMixin, login_required, login_user, flash, current_user, logout_user


class Auth (object):
    def __init__(self, app):
        """Static initialization"""
        self.app = app
        self.login_manager = LoginManager ()
        self.login_manager.init_app (app)
        self.login_manager.user_loader (self.load_user)

        self.users = { }

    def login_user (self, user):
        """Login given user"""
        if user is not None:
            self.users[user.session_id] = user
            return login_user (user)
        return None

    def load_user (self, session_id):
        """Loads user by user_id or return None"""

        if session_id in self.users:
            return self.users[session_id]
        return None


    def logout_user (self):
        """Logout current user"""
        return logout_user ()


class SessionUser (UserMixin):
    def __init__(self, user, session_id):
        self.session_id = self.id = session_id
        self.user = user