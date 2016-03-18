import paho.mqtt.client as mqtt

# set up the mqtt client
mqttc = mqtt.Client("python_pub")

# the server to publish to, and corresponding port
mqttc.connect("192.168.1.131", 1883)

# the topic to publish to, and the message to publish
mqttc.publish("homation/livingRoom/lights/Celling", "OK from Kepler")

# establish a two-second timeout
mqttc.loop(2)