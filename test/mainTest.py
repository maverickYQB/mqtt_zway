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

print "Out_going topic: ", outgoing_topic
print "On_going topic: " , ongoing_topic
print "Mqtt addres: ", mqtt_ip
print "Mqtt port: ", mqtt_port
print zway_ip
print zway_port
print dev_dict

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("COnnected to MQTT server "+str(rc))

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

mqttc = mqtt.Client("openhab")
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message

mqttc.connect(mqtt_ip, mqtt_port)
mqttc.subscribe(ongoing_topic, qos=1)
mqttc.loop_start() #start new thread

while True:
    try:
        print mqtt_zway.devdict_get(zway_ip,zway_port)
        time.sleep(5)
    except Exception:
        pass
'''

while True:
    try:
        mqtt_zway.dev_poll(dev_dict)
    except Exception:
        pass
'''