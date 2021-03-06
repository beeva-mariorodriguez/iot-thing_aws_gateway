#!/usr/bin/env python

import paho.mqtt.client as mqtt
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import getopt
import uuid

def connect_to_mqtt(mqttaddr,mqttport):
    """ connect to MQTT and return client """

    # callbacks
    def on_connect(client,userdata,flags,rc):
        """ exit(1) if connect to MQTT fails """
        if rc != 0:
            print("connection to MQTT failed: " + connack_string(rc))
            exit(1)
        else:
            print('connected to MQTT!')

    print("connecting to {}:{}".format(mqttaddr,mqttport))
    c = mqtt.Client()
    c.on_connect = on_connect
    c.connect(mqttaddr, mqttport, keepalive=60)
    return c

# callbacks
def on_message(client, userdata, message):
    print('received message on topic: {}'.format(message.topic))
    print('\tmessage: {}'.format(message.payload))
    mqttClient.publish(
        message.topic,
        str(message.payload),
        1)   # QoS
    print('\tmessage sent to MQTT!')

def connect_to_aws_iot(clientid,endpoint):
    """ connect to AWS IoT and return client """

    print "clientid: " + clientid 
    c = AWSIoTMQTTClient(clientid)
    c.configureEndpoint(endpoint, 8883)
    c.configureCredentials(
        rootCAPath,
        privateKeyPath,
        certificatePath)
    c.configureOfflinePublishQueueing(-1)
    c.configureDrainingFrequency(2)
    c.configureConnectDisconnectTimeout(10)
    c.configureMQTTOperationTimeout(5)
    print("connecting to AWS IoT")
    if not c.connect():
        print("unable to connect to AWS IoT")
        exit(1)
    print("connectted to AWS IoT")
    return c

# Help info
helpInfo = """usage:
    -e, --endpoint aws IoT endpoint
    -r, --rootCA   root CA file path
    -c, --cert     certificate file path
    -k, --key      private key file path
    -t, --topic    topic, default: '*'
    -m, --mqtt     mqtt server, default: 127.0.0.1
    -p, --port     mqtt port, default: 1883
    -h, --help
"""

endpoint = ""
rootCAPath = ""
certificatePath = ""
privateKeyPath = ""
topic = '*'
mqttaddr = "127.0.0.1"
mqttport = 1883

try:
    opts, args = getopt.getopt(sys.argv[1:], "he:k:c:r:t:m:p:", ["help", "endpoint=", "key=","cert=","rootCA=","mqtt=","port="])
    if len(opts) == 0:
        raise getopt.GetoptError("No input parameters!")
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(helpInfo)
            exit(0)
        elif opt in ("-e", "--endpoint"):
            endpoint = arg
        elif opt in ("-r", "--rootCA"):
            rootCAPath = arg
        elif opt in ("-c", "--cert"):
            certificatePath = arg
        elif opt in ("-k", "--key"):
            privateKeyPath = arg
        elif opt in ("-t", "--topic"):
            topic = arg
        elif opt in ("-m", "--mqtt"):
            mqttaddr = arg
        elif opt in ("-p", "--port"):
            mqttport = int(arg)
except getopt.GetoptError:
    print(helpInfo)
    exit(1)

awsMQTTClient = connect_to_aws_iot(str(uuid.uuid4()),endpoint)
mqttClient = connect_to_mqtt(mqttaddr,mqttport)

print("subscribe to {}".format(topic))
awsMQTTClient.subscribe(topic,0, on_message)

while True:
    pass

