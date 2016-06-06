#!/usr/bin/env python
'''
Created on Mars 20 2016

@author: popotvin
'''

import config
import mqtt_zway
import json
import paho.mqtt.client as mqtt
import time
import datetime

date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# MQTT config
outgoing_topic = config.get("TOPICS","outgoing_topic")
ongoing_topic = config.get("TOPICS","ongoing_topic")
mqtt_ip = config.get("MQTT_BROKER","mqtt_ip")
mqtt_port = config.get("MQTT_BROKER","mqtt_port")
mqtt_old_payload = []
mqtt_new_payload = []
payload = {}

# ZWAY config
zway_ip = config.get("ZWAY","zway_ip")
zway_port = config.get("ZWAY","zway_port")

# Update a list of connected devices on the zway server
zway_devList = mqtt_zway.zway_devList(zway_ip,zway_port)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print "Connected to MQTT server "+ date_time
    client.subscribe(ongoing_topic)

# The callback for when a SUBCRIBED message is received to the server.
def on_subscribe(client, userdata, mid, granted_qos):
    print "Subscribed to MQTT topic: " + str(ongoing_topic)+" QOS = " + str(granted_qos), date_time

# The callback for when a PUBLISH message is received from the server.
'''
    Lorsque je publie en utilisant la class le main loop arrete a verifier.... 2016-06-05
'''
def on_message(client, userdata, msg):
    print (msg.topic+" "+str(msg.payload))
    json_string = str(msg.payload)
    ongoing_id = "3"
    ongoing_type = "SwitchMultilevel"
    ongoing_value = str(json_string)
    zway_devList.dev_set(ongoing_id, ongoing_type, ongoing_value)


mqttc = mqtt.Client("openhab")
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect(mqtt_ip, mqtt_port)
mqttc.loop_start()  # start new thread

# Test zway and MQTT servers
zway_test = mqtt_zway.server_test(zway_ip, zway_port)
mqtt_test = mqtt_zway.server_test(mqtt_ip, mqtt_port)

# Main loop
if zway_test and mqtt_test:
    print "ZWAY is online!!!", date_time
    print "MQTT is online!!!", date_time
    while True:
        try:
            for key, value in zway_devList.dev_dict().iteritems():
                for i,j in value.iteritems():
                    if i == "id":
                        dev_id = j
                    elif i == "type":
                        dev_type = j
                zway_devList.dev_get(dev_id, dev_type)
                time.sleep(0.1)
                payload["device_id"] = str(dev_id)
                payload["type"] = str(dev_type)
                payload["value"] = str(zway_devList.dev_value(dev_id, dev_type))
                mqtt_new_payload.append(dict(payload))
                time.sleep(0.1)
            if mqtt_old_payload != mqtt_new_payload:
                mqttc.publish(outgoing_topic, str(mqtt_new_payload))
                print "published to mQTT", mqtt_new_payload
            mqtt_old_payload = mqtt_new_payload
            mqtt_new_payload = []
            time.sleep(1)

        except Exception:
            break

elif not zway_test:
    print "ZWAY server is offline"
elif not mqtt_test:
    print "MQTT server is Offline"

