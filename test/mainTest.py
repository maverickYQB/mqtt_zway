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
            payload["value"] = str(mqtt_zway.dev_data(zway_ip,zway_port,id,type))
            print "payload = ",payload
            mqtt_new_payload.append(payload)
            time.sleep(0.1)
        print ("new Payload: "+str(mqtt_new_payload))
        print ("old Payload: "+str(mqtt_old_payload))
        if mqtt_old_payload != mqtt_new_payload:
            mqttc.publish(outgoing_topic, str(mqtt_new_payload))
        mqtt_old_payload = mqtt_new_payload
        mqtt_new_payload = []
        time.sleep(3)

    except Exception:
        pass
