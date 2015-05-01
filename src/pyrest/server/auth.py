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
        self.check_credentials = None


    def login (self, username, password=None, key=None):
        """
        Method will generate session id for user
        and create and return User object
        If check_credentials is set
        it will be called
        """
        session_id = str (uuid.uuid4 ())
        user = User (session_id)
        user.username = username
        user.password = password
        user.key = key

        if self.check_credentials is not None and self.check_credentials (user):
            return user
        elif self.check_credentials is None:
            return user

        return None

    def login_user (self, user):
        """Login given user"""
        if user is not None:
            self.users[user.id] = user
            return login_user (user)
        return None

    def load_user (self, user_id):
        """Loads user by user_id or return None"""
        if user_id in self.users:
            return self.users[user_id]
        return None


    def logout_user (self):
        """Logout current user"""
        return logout_user ()


class User (UserMixin):
    def __init__ (self, session_id):
        self.id = session_id


