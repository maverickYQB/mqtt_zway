#!/usr/bin/env python
'''
Created on Feb 4, 2016

@author: popotvin
'''
import requests
import json
import paho.mqtt.client as mqtt
import time


def devPoll(dev_dict):
    old_payload = []
    new_payload = []
    for key, value in dev_dict.iteritems():
        print ("device: "+key)
        for i,j in value.iteritems():
            if (i == "ip"):
                ip = j
            elif (i =="id"):
                id = j
            elif(i == "type"):
                type = j
            elif(i == "port"):
                port = j
        devGet(id,type,ip,port)
        time.sleep(0.1)
        payload = "nodeID: " +id+ " type: " +type+ " value: "+str(devData(id,type,ip,port))
        print (payload)
        new_payload.append(payload)
        time.sleep(0.1)
    print ("new Payload: "+str(new_payload))
    print ("old Payload: "+str(old_payload))
    if old_payload != new_payload:
        mqttc.publish(topicOutgoing, str(new_payload))
    old_payload = new_payload
    newPayload = []
    time.sleep(3)