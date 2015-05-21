# encoding: utf-8
# author:   Jan Hybs
import codecs
import sys, os

from pyrest import app
from flask import redirect, render_template, g
from pyrest.server.flask_utils import with_tittle


@app.route ('/')
@with_tittle ('PyRest::home')
def main ():
    """
    Main view which shows almost nothing
    """
    import markdown
    input_file = codecs.open("../README.md", mode="r", encoding="utf-8")
    text = input_file.read()
    html = markdown.markdown(text)
    return render_template ('main.html', content=html)