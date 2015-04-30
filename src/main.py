import time, random

from flask import Flask, render_template, request, escape, redirect, url_for
from flask_socketio import SocketIO, send, emit
from flask_login import LoginManager, UserMixin, login_required, login_user, flash, current_user, logout_user
from auth import Auth, authenticated_only

app = Flask (__name__)
app.config['SECRET_KEY'] = 'secretcacas!'

socket = SocketIO (app)
auth = Auth (app)


@app.route ("/login/<username>")
def login (username):
    user = auth.login (username)
    if user is None:
        return "wrong credentials"

    auth.login_user (user)

    print 'login user ' + user.username
    print 'login id' + user.id
    return redirect ('/')


@app.route ("/logout")
def logout ():
    auth.logout_user ()
    return redirect ('/')


@app.route ('/')
def main ():
    return render_template ('main.html')


@socket.on ('connect')
def ws_conn ():
    socket.emit ('msg', 'co co')


@socket.on ('disconnect')
def ws_disconn ():
    socket.emit ('msg', 'disco')


@socket.on ('city')
@authenticated_only
def ws_city (message):
    # print message['city']
    emit ('city', { 'city': escape (current_user.username + ": " + message['city']) })
    auth = current_user.is_authenticated ()
    emit ('msg', str (auth))

    # i = 1
    # while True:
    # i+=1
    # time.sleep (1)
    # emit('city', {'city': r}, broadcast=False)


if __name__ == '__main__':
    app.debug = True
    socket.run (app, host='0.0.0.0', port=5000)

    # @app.route('/', methods=['GET', 'POST'])
    # def index():
    # if request.method == 'POST':
    # return "POST req"
    # else:
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