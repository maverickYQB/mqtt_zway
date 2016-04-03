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
import datetime

date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
    print "Connected to MQTT server "+ date_time.now()
    client.subscribe(ongoing_topic)

# The callback for when a SUBCRIBED message is received to the server.
def on_subscribe(client, userdata, mid, granted_qos):
    print "Subscribed to MQTT topic: "+str(ongoing_topic)+" QOS = "+str(granted_qos), date_time.now()

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print (msg.topic+" "+str(msg.payload))
    json_string = json.loads(msg.payload.replace("\'", '"'))
    if msg.topic == ongoing_topic:
        device_id = json_string["device_id"]
        type =  json_string["type"]
        value = json_string["value"]
        mqtt_zway.dev_set(zway_ip,zway_port,device_id,type,value)
    else:
        print "Wrong topic sent"

mqttc = mqtt.Client("openhab")
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message
mqttc.on_connect = on_connect

mqttc.connect(mqtt_ip, mqtt_port)
mqttc.loop_stop() #start new thread

zway_test = mqtt_zway.server_test(zway_ip, zway_port)
mqtt_test = mqtt_zway.server_test(mqtt_ip, mqtt_port)

if zway_test == True:
    print "zway is online!!!", date_time
else:
    print "zway is offline"

if mqtt_test == True:
    print "MQTT is online!!!", date_time
else:
    print "MQTT is offline"

#Main loop
while True:
    try:
        for key, value in dev_dict.iteritems():
            for i,j in value.iteritems():
                if (i =="id"):
                    id = j
                elif(i == "type"):
                    type = j
            mqtt_zway.dev_get(zway_ip,zway_port,id,type)
            time.sleep(0.1)
            payload["device_id"] = str(id)
            payload["type"] =  type
            payload["value"] = str(mqtt_zway.dev_value(zway_ip,zway_port,id,type))
            mqtt_new_payload.append(dict(payload))
            time.sleep(0.1)
        if mqtt_old_payload != mqtt_new_payload:
            mqttc.publish(outgoing_topic, str(mqtt_new_payload))
            print "published to mQTT", mqtt_new_payload
        mqtt_old_payload = mqtt_new_payload
        mqtt_new_payload = []
        time.sleep(1)

    except Exception:
        pass
