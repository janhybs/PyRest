import time, random
import uuid
from flask import Flask, render_template, request, escape, redirect, url_for
from flask_socketio import SocketIO, send, emit
from flask_login import LoginManager, UserMixin, login_required, login_user, flash, current_user, logout_user
import functools

app = Flask (__name__)
app.config['SECRET_KEY'] = 'secretcacas!'
socketio = SocketIO (app)
login_manager = LoginManager ()
login_manager.init_app (app)

users = {}

def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated():
            print 'User not authenticated!'
            request.namespace.disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped

class User(UserMixin):
    def __init__(self, username, session_id):
        self.username = username
        self.id = session_id


@login_manager.user_loader
def load_user(userid):
    if userid in users:
        return users[userid]
    return None



@app.route("/login/<username>")
def login(username):
    session_id = str(uuid.uuid4 ())
    user = User (username, session_id)
    login_user (user)

    users[str(session_id)] = user
    print 'login user ' + username
    print 'login id' + session_id
    return redirect('/')

@app.route("/logout")
def logout():
    logout_user ()

@app.route('/')
def main():
    return render_template('main.html')

@socketio.on('connect')
def ws_conn():
    socketio.emit('msg', 'co co')


@socketio.on('disconnect')
def ws_disconn():
    socketio.emit('msg', 'disco')

@socketio.on('city')
@authenticated_only
def ws_city(message):
    # print message['city']
    emit ('city', {'city': escape(current_user.username + ": " + message['city'])})
    auth = current_user.is_authenticated()
    emit ('msg', str(auth))

    # i = 1
    # while True:
    #     i+=1
    #     time.sleep (1)
    #     emit('city', {'city': r}, broadcast=False)

if __name__ == '__main__':
    app.debug = True
    socketio.run(app, host='0.0.0.0', port=5000)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         return "POST req"
#     else:
#         return "GET req"
#
# @app.route('/hello')
# def hello():
#     return 'Hello World'
#
#
# @app.route('/user/<username>')
# def show_user_profile(username):
#     # return render_template('main.html', name=username, p=request.form['username']) 400 bad request
#     return render_template('main.html', name=username,)
#
# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     # show the post with the given id, the id is an integer
#     return 'Post %d' % post_id
#
#
#
# @app.route('/projects/')
# def projects():
#     return 'The project page'
#
# @app.route('/about')
# def about():
#     return 'The about page'
#
# @sockets.route('/test')
# def test_connect(ws):
#     while True:
#         message = ws.receive()
#         ws.send(message)
#
# if __name__ == '__main__':
#     app.run(debug=True)
#     # app.run(host='0.0.0.0')