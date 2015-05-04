# encoding: utf-8
# author:   Jan Hybs

from pyrest import app, socket, auth, database, with_tittle
from flask import redirect, render_template, g



@app.route ('/')
@with_tittle ('PyRest::home')
def main ():
    return render_template ('main.html')


@app.route('/success', methods=['GET', 'POST'])
def on_login ():
    return 'foo'