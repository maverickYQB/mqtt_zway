#!/usr/bin/env python
'''
Created on Feb 4, 2016

@author: popotvin
'''

import os
import ConfigParser

'''
    Return the config section and option from the config file.
    e.g.
        [SECTION]
        option1 = val1
        option2 = val2
'''

def get(section, option):
    file = os.path.join(os.path.dirname(__file__), 'Config.cfg')
    config = ConfigParser.ConfigParser()
    config.read(file)
    return config.get(section,option)

