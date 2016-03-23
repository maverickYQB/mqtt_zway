#!/usr/bin/python
'''
Created on Feb 4, 2016

@author: popotvin
'''
import requests
import json
import paho.mqtt.client as mqtt
import time
from mqtt_zway import devPoll

'''Dict. of the zwave light switches (later it will be a mqtt json payload)
'''
devList =    {
              "device1":{"id":"2","type":"SwitchMultilevel","ip":"192.168.1.131","port":"8083"},
              "device2":{"id":"3","type":"SwitchMultilevel","ip":"192.168.1.131","port":"8083"},
              "device3":{"id":"4","type":"Basic","ip":"192.168.1.131","port":"8083"}
              #"device4":{"id":"6","type":"SwitchMultilevel","ip":"192.168.1.131","port":"8083"}
              }

#MQTT topic to publish
topicOutgoing = "openhab/zwave/lighting"
topicOngoing = "zwave/lighting"

#ZWAY IP/PORT:
zwayIP = "192.168.1.131"
zwayPORT = "8083"

#MQTT broker IP/PORT
mqttIP = "192.168.1.131"
mqttPORT = 1883


#Search the connected zwave devices on the z-way REST server
def devFind(ip,port):
    url = "http://"+ip+":"+port+"/ZWaveAPI/Data/*"
    response = requests.post(url)
    data = response.json()
    devList = {}
    
    if data != None:
        for i in data["devices"]:
            if i != "1":    #Device_1 is main controller
                devList[i] = data["devices"][""+i+""]["data"]["deviceTypeString"]["value"]
                
        return (devList)

#zway server REST API get() to refresh the value of the zwave light switches.
def devGet(id,type,ip,port):
    data = ""
    url = "http://"+ip+":"+port+"/ZWaveAPI/Run/devices["+id+"].instances[0]."+type+".Get()"
    response = requests.post(url)
    data = response.json()
    print("Get() id: "+id+ " Value: "+str(data))    

#zway server REST API get() to read the value of the zwave light switches.
def devData(id,type,ip,port):
    url = ("http://"+ip+":"+port+"/ZWaveAPI/Run/devices["+id+"].instances[0]."+type+".data.level.value")
    response = requests.post(url)
    value = response.json()
    print ("value: ""\n""id: "+id+"\n""Value: "+str(value)+"\n")
    return value

'''
Iterate thru the devices list Dict.
and update the light switch values. The values are only 
published on changed value to the MQTT broker.

to do separer les def en class p-e car je call une function dans une fonction....
'''

def devPoll(devList):
    oldPayload = []
    newPayload = []
    for key, value in devList.iteritems():
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
        newPayload.append(payload)
        time.sleep(0.1)
    print ("new Payload: "+str(newPayload))
    print ("old Payload: "+str(oldPayload))
    if oldPayload != newPayload:
        mqttc.publish(topicOutgoing, str(newPayload))
    oldPayload = newPayload
    newPayload = []
    time.sleep(3)
'''
to do:Sortir le if new old payload le mettre dans  le main script et retourner un payload a la place
'''
      
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))    
    
# set up the mqtt client
mqttc = mqtt.Client("openhab")
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message

mqttc.connect(mqttIP, mqttPORT)
mqttc.subscribe(topicOngoing, qos=1)
mqttc.loop_start() #start new thread 

while True:
    try:
        devList = devFind(zwayIP,zwayPORT)
        print (devList)
        if devList != None:
            devPoll(devList)
    except Exception: 
        pass
    
    
'''
To DO:
Finir de batir le devList avec devFind afin de pouvoir prendre le dict. devList pour lancer devPoll
revoir le tout pour faire une class et constructeur d'objet
'''
