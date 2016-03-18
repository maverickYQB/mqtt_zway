#!/usr/bin/python
'''
Created on Mar 7, 2016

@author: popotvin
'''
import os
from ConfigParser import SafeConfigParser

print os.getcwd()
print os.path.abspath(__file__)


file_path = os.path.abspath("config/config.cfg")
print file_path

parser = SafeConfigParser()
parser.read(file_path)


print parser.get('Configuration', 'publish_topic')