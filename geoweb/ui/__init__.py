#!/usr/bin/python
# -*- coding: utf-8 -*-

""" __init__.py : __init__.py """

from .controllers import UI

__author__ = "Abhay Arora (@BzFTMxc)"


blueprints = [UI]

def bind(app):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
