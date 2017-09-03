#!/usr/bin/python
# -*- coding: utf-8 -*-

""" controllers.py : controllers.py """

from flask import Blueprint
from flask import render_template
import os

__author__ = "Abhay Arora (@BzFTMxc)"


UI = Blueprint('UI', __name__, template_folder='views')


@UI.route('/')
def index():
    return render_template('geoweb.jade')


@UI.route('/view/<view_name>')
def view(view_name):
    try:
        ret = render_template(view_name + '.jade')
    except:
        try:
            fn = '/views/' + view_name + '.html'
            ret = send_file(os.path.dirname(__file__) + fn)
        except:
            ret = ''
    return ret
