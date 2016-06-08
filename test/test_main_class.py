#!/usr/bin/env python
'''
Created on Mars 20 2016

@author: popotvin
'''

import mqtt_zway_test
import mqtt_zway
import paho.mqtt.client as mqtt
import time
import traceback

date_time = mqtt_zway_test.date_time

# Main variables
mqtt_old_payload = []
mqtt_new_payload = []
payload = {}
publish_string = ""

# MQTT config
outgoing_topic = mqtt_zway_test.outgoing_topic
ongoing_topic = mqtt_zway_test.ongoing_topic
mqtt_ip = mqtt_zway_test.mqtt_ip
mqtt_port = mqtt_zway_test.mqtt_port
mqtt_client = mqtt_zway_test.mqtt_client

# ZWAY config
zway_ip = mqtt_zway_test.zway_ip
zway_port = mqtt_zway_test.zway_port

# list of connected devices on the zway server (device_id, device type, device level value)
zway_devList = mqtt_zway.zway_devList(zway_ip,zway_port)

# MQTT Client init
mqttc = mqtt.Client(str(mqtt_client))
mqttc.on_subscribe = mqtt_zway_test.on_subscribe
mqttc.on_message = mqtt_zway_test.on_message
mqttc.on_connect = mqtt_zway_test.on_connect
mqttc.connect(mqtt_ip, mqtt_port)

# Test zway and MQTT servers
zway_test = mqtt_zway.server_test(zway_ip, zway_port)
mqtt_test = mqtt_zway.server_test(mqtt_ip, mqtt_port)

# Main loop
if zway_test and mqtt_test:
    print "ZWAY is running at: %s"% str(date_time)
    print "MQTT is running at: %s"% str(date_time)
    while True:
        try:
            mqttc.loop()
            for key, value in zway_devList.dev_dict().iteritems():
                for i,j in value.iteritems():
                    if i == "id":
                        dev_id = j
                    elif i == "type":
                        dev_type = j
                zway_devList.dev_get(dev_id, dev_type)
                payload["device_id"] = str(dev_id)
                payload["type"] = str(dev_type)
                payload["value"] = zway_devList.dev_value(dev_id, dev_type)
                mqtt_new_payload.append(dict(payload))
                time.sleep(0.1)
            if mqtt_old_payload != mqtt_new_payload:
                mqttc.publish(outgoing_topic, str(mqtt_new_payload))
                #print "published to mQTT: %s" % mqtt_new_payload
            mqtt_old_payload = mqtt_new_payload
            mqtt_new_payload = []
            time.sleep(0.5)
        except Exception, e:
            print traceback.print_exc()
            break

elif not zway_test:
    print "ZWAY server is offline"
elif not mqtt_test:
    print "MQTT server is Offline"

