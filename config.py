#!/usr/bin/env python
'''
Created on Feb 4, 2016

@author: popotvin
'''
import requests
import os
from ConfigParser import SafeConfigParser
import paho.mqtt.client as mqtt


def config():
    #mydir = os.path.dirname(os.path.abspath(__file__))
    #file_path = os.path.join(mydir, '..', "/config/config.cfg")
    mydir = os.path.join(os.path.abspath(__file__))
    print "mydir"+mydir
    print "CWD"+os.getcwd()
    path = os.path.abspath(__file__)
    print "abs_PATH: " + path
    file = os.path.join(os.path.dirname(__file__), 'Config.cfg')
    config = SafeConfigParser()
    config.read(file)
    print config.sections()
    #print file.read()
    '''
    config = SafeConfigParser()
    configFile = os.path.abspath("Config.cfg")
    config.read(configFile)
    print configFile
    print config.sections()
    file = open(os.path.join(path,(configFile, "r")))
    print file.read()
'''
config()