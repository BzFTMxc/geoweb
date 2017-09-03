#!/usr/bin/python
# -*- coding: utf-8 -*-

""" controllers.py : controllers.py """

from flask import Blueprint
from flask import jsonify
from flask import current_app as app
import os

__author__ = "Abhay Arora (@BzFTMxc)"


API = Blueprint('API', __name__, url_prefix='/api')

@API.route('/stats/sam')
def list_sams():
    sam_list = []
    try:
        data_dir = app._CONF.get('storage', 'data_dir')
    except:
        return jsonify(dict(
            status='ERR',
            data=[],
            errors=['Storage path not set.']
        ))
    try:
        dirs = os.listdir(data_dir)
        return jsonify(dict(
            status='OK',
            data=dirs
        ))
    except:
        return jsonify(dict(
            status='ERR',
            data=['Could not search for SAMs.']
        ))

@API.route('/layer/<sam>/<layer>')
def get_layer(sam, layer):
    return jsonify(dict(
        sam=sam,
        layer=layer
    ))
