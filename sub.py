#!/usr/bin/env python

import paho.mqtt.client as mqtt
from mqttclass import *
import time

# The callback for when a PUBLISH message is received from the server.
def on_message_sensor(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	
	
# The callback for when a PUBLISH message is received from the server.
def on_message_cmd(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))

def mk_cmd():
	return {'cmd':'s'}

s = SubJSON('sensors',on_message_sensor)
s.start()

c = PubJSON('cmds')
c.start()

while True:
	time.sleep(1)
	c.publish( mk_cmd() )
	pass