#!/usr/bin/python
# -*- coding: utf-8 -*-

""" __init__.py : __init__.py """

from flask import Flask
from pyjade.ext.jinja import PyJadeExtension
import os

from .modules import __all__ as modules

__author__ = "Abhay Arora (@BzFTMxc)"

def create_app(config, modules=modules):
    app = Flask(__name__,
                static_folder=os.path.dirname(__file__) + '/../static')
    app.jinja_env.add_extension(PyJadeExtension)

    app._CONF = config

    for module in modules:
        module.bind(app)
    
    return app
