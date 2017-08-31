#!/usr/bin/python
# -*- coding: utf-8 -*-

""" __init__.py : __init__.py """

from flask import Flask
from pyjade.ext.jinja import PyJadeExtension
import os

from ui import module as UI
from api import module as API

__author__ = "Abhay Arora (@BzFTMxc)"


modules = [UI, API]

def create_app(config, modules=modules):
    app = Flask(__name__,
                static_folder=os.path.dirname(__file__) + '/../static')
    app.jinja_env.add_extension(PyJadeExtension)

    for module in modules:
        module.bind_to(app)
    
    return app
