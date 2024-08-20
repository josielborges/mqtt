import os

import paho.mqtt.client as paho
from dotenv import load_dotenv
from paho import mqtt

load_dotenv()

# Configurações do broker
broker_url = os.getenv('BROKER_URL')
broker_port = int(os.getenv('BROKER_PORT'))
broker_user = os.getenv('BROKER_USER')
broker_password = os.getenv('BROKER_PASSWORD')
topic = "my_topic/test"


# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)


# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))


# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv311)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set(broker_user, broker_password)
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect(broker_url, broker_port)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe(topic + "/#", qos=1)

# a single publish, this can also be done in loops, etc.
client.publish(topic, payload="hot", qos=1)

# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
client.loop_forever()