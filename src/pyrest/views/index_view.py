# encoding: utf-8
# author:   Jan Hybs

from pyrest import app
from flask import redirect, render_template, g
from pyrest.server.flask_utils import with_tittle


@app.route ('/')
@with_tittle ('PyRest::home')
def main ():
    """
    Main view which shows almost nothing
    """
    return render_template ('main.html')