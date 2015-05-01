# encoding: utf-8
# author:   Jan Hybs

from pyrest import app, socket, auth, database
from flask import redirect, render_template


@app.route ('/')
def main ():
    return render_template ('main.html')