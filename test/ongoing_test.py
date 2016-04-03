#!/usr/bin/env python
'''
Created on Feb 4, 2016
as
@author: popotvin
'''

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
mqtt_old_payload = []
mqtt_new_payload = []
payload = {}

#ZWAY config
zway_ip = config.get("ZWAY","zway_ip")
zway_port = config.get("ZWAY","zway_port")

#Update a list of connected devices on the zway server
dev_dict = mqtt_zway.devdict_get(zway_ip,zway_port)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("COnnected to MQTT server "+str(rc))

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print (msg.topic+" "+str(msg.payload))


mqttc = mqtt.Client()
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message
mqttc.on_connect = on_connect

mqttc.connect(mqtt_ip, mqtt_port)
mqttc.subscribe(ongoing_topic, qos=1)
mqttc.loop_forever() #start new thread

'''
  json_string = json.loads(msg.payload.replace("\'", '"'))
    if msg.topic == ongoing_topic:
        device_id = json_string["device_id"]
        type =  json_string["type"]
        value = json_string["value"]
        mqtt_zway.dev_set(zway_ip, zway_port, device_id, type, value)
    else:
        print "Wrong topic sent"
'''