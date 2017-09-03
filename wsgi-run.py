#!/usr/bin/python
# -*- coding: utf-8 -*-

""" wsgi-run.py : wsgi-run.py """

from geoweb import create_app
from configparser import ConfigParser
import os

__author__ = "Abhay Arora (@BzFTMxc)"

config = ConfigParser()
config.read(os.path.dirname(os.path.abspath(__file__)) +\
            '/config/geoweb.ini')

app = create_app(config)

if __name__ == '__main__':
    is_debug_mode = False
    try:
        debug_conf = config.get('server', 'debug')
        if debug_conf.lower() == 'true':
            is_debug_mode = True
    except:
        pass
    server_host = '0.0.0.0'
    try:
        server_host = config.get('server', 'host')
    except:
        pass
    server_port = 2501
    try:
        server_port = int(config.get('server', 'port'))
    except:
        pass
    app.run(debug=is_debug_mode,
            host=server_host,
            port=server_port)
