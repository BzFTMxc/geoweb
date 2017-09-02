#!/usr/bin/python
# -*- coding: utf-8 -*-

""" controllers.py : controllers.py """

from flask import Blueprint

__author__ = "Abhay Arora (@BzFTMxc)"


UI = Blueprint('UI', __name__)

@UI.route('/')
def index():
    return 'TEST'

