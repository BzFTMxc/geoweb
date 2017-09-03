#!/usr/bin/python
# -*- coding: utf-8 -*-

""" load_gml.py : load_gml.py """

'''
Temporarily created python script to load GML
data to the application. Will replace later with
a user interface.
@TODO: add WebUI for data loading.
@TODO: add support for more formats.
'''

from lxml import objectify
from lxml.objectify import ObjectifiedElement
from configparser import ConfigParser
import sys
import re
import json
import os

__author__ = "Abhay Arora (@BzFTMxc)"


if len(sys.argv) < 2:
    print '\nMissing required parameters!\nUsage: load_gml.py <path-to-gml>\n'
    exit(1)

gml = None
try:
    gml = objectify.parse(sys.argv[1])
except:
    print 'Could not read GML!\n Error while reading ' + sys.argv[1] + '.'
    exit(1)


#
# Read configs
#
config = ConfigParser()
try:
    config.read(os.path.dirname(os.path.abspath(__file__)) +\
                '/config/geoweb.ini')
except:
    print('Could not read config!\n')
    exit()


# 
# Iterates xml and generates dict.
# XML hierarchy not persisted in dict. Need to fix.
# 
# @TODO: rewrite function to iterate single depth level
# 
def to_dict(node):
    iterator = node.iter()
    _self = iterator.next()
    data = dict()
    while True:
        try:
            _next = iterator.next()
            if type(_next) is ObjectifiedElement:
                continue
                # data[re.sub(r'{.*}', '', _next.tag)] = to_dict(_next)
                # @TODO: Enable above written recursion
                #        after solving iteration depth issue 
            else:
                data[re.sub(r'{.*}', '', _next.tag)] = _next.text
        except:
            break
    return data


# ------------------------
# Initialize SAM directory
# ------------------------
data_dir = config.get('storage', 'data_dir')
sam_name = str(gml.getroot().iter().next().header.requestID.text)
if not os.path.exists(os.path.join(data_dir, sam_name)):
    os.makedirs(os.path.join(data_dir, sam_name))
sam_dir = os.path.join(data_dir, sam_name)
    
#
# Dumps GML data into JSON file
# Uses to_dict() function
#
def dump_json(node, tag, file_path=None):
    elems = gml.iter(tag)
    elems_data = dict(
        element=re.sub(r'{.*}', '', tag),
        data=[]
    )
    while True:
        try:
            elem = elems.next()
            elems_data['data'].append(to_dict(elem))
        except:
            break
    if file_path is None:
        file_path = os.path.join(sam_dir, re.sub(r'{.*}', '', tag) + '.json')
    elems_file = open(file_path, 'w')
    elems_file.write(json.dumps(elems_data))
    elems_file.close()



#
# Dump required data
#
dump_json(gml, r'{http://www.telstra.com.au/nbn}coaxialCable')
dump_json(gml, r'{http://www.telstra.com.au/nbn}structureRoute')
dump_json(gml, r'{http://www.telstra.com.au/nbn}structurePoint')
