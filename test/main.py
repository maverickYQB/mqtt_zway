#!/usr/bin/env python
'''
Created on Feb 4, 2016

@author: popotvin
'''
import requests
import os
from ConfigParser import SafeConfigParser
import paho.mqtt.client as mqtt


def config_test():
    mydir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(mydir, '..', "/config/config.cfg")

    parser = SafeConfigParser()
    parser.read(file_path)


    print parser.get('topicOutgoing', 'topicOngoing') # erreur a corriger

config_test()