#!/usr/bin/env python
'''
Created on Feb 4, 2016

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
dev_list = mqtt_zway.devlist_get(zway_ip,zway_port)

print outgoing_topic
print ongoing_topic
print mqtt_ip
print mqtt_port
print zway_ip
print zway_port
print dev_list


#to be the main loop
'''
# set up the mqtt client
mqttc = mqtt.Client("openhab")
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message

mqttc.connect(mqttIp, mqttPort)
mqttc.subscribe(topicOngoing, qos=1)
mqttc.loop_start() #start new thread


while True:
    try:
        devPoll(zwayDev)
    except Exception:
        pass
'''