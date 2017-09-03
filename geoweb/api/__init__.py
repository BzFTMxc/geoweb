#!/usr/bin/python
# -*- coding: utf-8 -*-

""" __init__.py : __init__.py """

from .controllers import API

__author__ = "Abhay Arora (@BzFTMxc)"


blueprints = [API]

def bind(app):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
