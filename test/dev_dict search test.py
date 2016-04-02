#!/usr/bin/env python
'''
Created on Feb 4, 2016
as
@author: popotvin
'''

import requests
import config
import mqtt_zway
import json
import paho.mqtt.client as mqtt
import time

#MQTT config
outgoing_topic = config.get("TOPICS","outgoing_topic")
ongoing_topic = config.get("TOPICS","ongoing_topic")
mqtt_ip = config.get("MQTT_BROKER","mqtt_ip")
mqtt_port = config.get("MQTT_BROKER","mqtt_port")

#ZWAY config
zway_ip = config.get("ZWAY","zway_ip")
zway_port = config.get("ZWAY","zway_port")

#Update a list of connected devices on the zway server
dev_dict = mqtt_zway.devdict_get(zway_ip,zway_port)

print dev_dict
payload = {}

for key, value in dev_dict.iteritems():
    for i,j in value.iteritems():
        if (i =="id"):
            id = j
        elif(i == "type"):
            type = j
    mqtt_zway.dev_get(zway_ip,zway_port,id,type)
    time.sleep(0.1)
    payload["device_id"] = id
    payload["type"] =  type
    payload["value"] = str(mqtt_zway.dev_data(zway_ip,zway_port,id,type))
    print "payload = ",payload