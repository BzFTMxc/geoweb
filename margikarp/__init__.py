#!/usr/bin/python
# -*- coding: utf-8 -*-

""" __init__.py : __init__.py """

from flask import Flask

def create_app(config):
    app = Flask(__name__)
    return app
