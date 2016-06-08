#!/usr/bin/env python
'''
Created on Feb 4, 2016

@author: popotvin
'''

import requests, socket
import datetime
import config
import json

date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# MQTT config
outgoing_topic = config.get("MQTT_TOPICS", "outgoing_topic")
ongoing_topic = config.get("MQTT_TOPICS", "ongoing_topic")
mqtt_ip = config.get("MQTT_BROKER", "mqtt_ip")
mqtt_port = config.get("MQTT_BROKER", "mqtt_port")
mqtt_client = config.get("MQTT_BROKER", "mqtt_client")

# ZWAY config
zway_ip = config.get("ZWAY","zway_ip")
zway_port = config.get("ZWAY","zway_port")

class zway_devList:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port

    def dev_dict(self):
        temp_dict = {}
        dev_dict = {}
        url = "http://"+self.ip+":"+self.port+"/ZWaveAPI/Data/*"
        response = requests.post(url)
        data = response.json()
        if data is not None:
            for i in data["devices"]:
                if i != "1":    # Device_1 is main controller
                    temp_dict["id"] = i
                    if "Multilevel" in data["devices"][""+i+""]["data"]["deviceTypeString"]["value"]:
                        temp_dict["type"] = "SwitchMultilevel"
                    elif "Binary" in data["devices"][""+i+""]["data"]["deviceTypeString"]["value"]:
                        temp_dict["type"] = "SwitchBinary"
                    dev_dict["device_"+i+""] = dict(temp_dict)
            return dict(dev_dict)

# Update the zwave light switches values.
    def dev_get(self,dev_id,dev_type):
        self.dev_id = dev_id
        self.dev_type = dev_type
        url = "http://"+self.ip+":"+self.port+"/ZWaveAPI/Run/devices["+self.dev_id+"].instances[0]."+self.dev_type+".Get()"
        # print "url %s" % (url)
        response = requests.post(url)
        data = response.json()
        return data

# Read the device level value of the zwave light switches.
    def dev_value(self,dev_id,dev_type):
        self.dev_id = dev_id
        self.dev_type = dev_type
        url = ("http://"+self.ip+":"+self.port+"/ZWaveAPI/Run/devices["+self.dev_id+"].instances[0]."+self.dev_type+".data.level.value")
        response = requests.post(url)
        value = response.json()
        # print ("value: ""\n""dev_id: "+dev_id+"\n""Value: "+str(value)+"\n")
        return str(value)
    
    def dev_set(self,dev_id,dev_type,dev_value):
        self.dev_id = dev_id
        self.dev_type = dev_type
        self.dev_value = dev_value
        url = ("http://"+self.ip+":"+self.port+"/ZWaveAPI/Run/devices["+self.dev_id+"].instances[0]."+self.dev_type+".Set("+self.dev_value+")")
        request = requests.post(url)
        data = request.json()
        return str(data)

# Server ping
def server_test(ip, port):
    s = socket.socket()
    try:
        s.connect((ip, int(port)))
        return True
    except Exception as e:
        return False
    finally:
        s.close()

# The callback for when the client receives a CONNACK response.
def on_connect(client, userdata, flags, rc):
    print "Connected to MQTT server at: %s" % str(date_time)
    client.subscribe(ongoing_topic)

# The callback for when a SUBCRIBED message is received
def on_subscribe(client, userdata, mid, granted_qos):
    print "Subscribed to MQTT topic: %s QOS = %s at: %s" % (str(ongoing_topic),str(granted_qos), str(date_time))

# The callback for when a PUBLISH message is received.
'''
    Note to myself for on_message function:
    - Need to ad verification to check if the input match the specific device from dev_list dictionary.
      e.g.: If the device is binary and the input type is "SwitchMultilevel" I need to raise an exception or
      at least a log entry ...
    - Code a for loop to run through nested JSON string.
'''
def on_message(client, userdata, msg):
    print (msg.topic+" "+str(msg.payload))
    json_string = json.loads(msg.payload)
    print "JSON: %s" % json_string
    dev_id = json_string["device_id"]
    dev_type = json_string["device_type"]
    dev_value = json_string["device_value"]
    url = ("http://" +zway_ip+ ":" +zway_port+ "/ZWaveAPI/Run/devices[" +dev_id+ "].instances[0]." +dev_type+ ".Set(" +dev_value+ ")")
    request = requests.post(url)
    data = request.json()
    return str(data)



    
    


       

