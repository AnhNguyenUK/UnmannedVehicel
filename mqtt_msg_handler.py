import re
import sys
import time
from queue import Queue
import threading
import paho.mqtt.client as paho
from paho import mqtt

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
    regex_pattern = r"Id: (.*),.*: (-?\d+.\d+).*: (-?\d+.\d+)"
    data = re.findall(regex_pattern, str(msg.payload))
    print(data[0])    

class HiveMqttServer:
    def __init__(self) -> None:
        self.host_url = "5fe2c1b3039c47afa0982607e636afc9.s1.eu.hivemq.cloud"
        self.port = 8883
        self.username = "mydev"
        self.password = "Thesis2022"
             
    def get_url(self):
        return self.host_url
    
    def get_port(self):
        return self.port
    
    def get_username(self):
        return self.username
    
    def get_password(self):
        return self.password
    
def print_sth_stupid():
    while(True):
        print("No no no")
# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client

q = Queue()

class mqttHandlingWorker:
    def __init__(self) -> None:
        self.client_pubKey = "5fe2c1b3039c47afa0982607e636afc9"
        self.client_url = "{}.s1.eu.hivemq.cloud".format(self.client_pubKey)
        self.client_port = 8883
        self.client.connect(self.client_url, self.client_port)
        self.subscribed_topic = "testing"

    def client_connect(self):
        self.client.on_connect = on_connect

        # enable TLS for secure connection
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        # set username and password
        self.client.username_pw_set("mydev", "Thesis2022")
        # connect to HiveMQ Cloud on port 8883 (default for MQTT)
        self.client.connect("5fe2c1b3039c47afa0982607e636afc9.s1.eu.hivemq.cloud", 8883)

        # setting callbacks, use separate functions like above for better visibility
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_disconnect = self.on_disconnect
        self.client.subscribe(self.subscribed_topic, qos=1)
    
    # setting callbacks for different events to see if it works, print the message etc.
    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("CONNACK received with code %s." % rc)

    # with this callback you can see if your publish was successful
    def on_publish(self, client, userdata, mid, properties=None):
        print("mid: " + str(mid))

    # print which topic was subscribed to
    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_message(self, client, userdata, msg):
        print(str(msg.payload))
        data = msg  
        regex_pattern = r"Id: (.*),.*: (-?\d+.\d+).*: (-?\d+.\d+)"
        data = re.findall(regex_pattern, str(msg.payload))
        q.put(list(data[0]))
        print("Data package: {}".format(data))
        # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    def on_disconnect(self, client, userdata,rc=0):
        print("DisConnected result code "+str(rc))
        client.loop_stop()

    
if __name__ == '__main__':

    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    client.on_connect = on_connect

    # enable TLS for secure connection
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    # set username and password
    client.username_pw_set("mydev", "Thesis2022")
    # connect to HiveMQ Cloud on port 8883 (default for MQTT)
    client.connect("5fe2c1b3039c47afa0982607e636afc9.s1.eu.hivemq.cloud", 8883)

    # setting callbacks, use separate functions like above for better visibility
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.on_publish = on_publish

    # subscribe to all topics of encyclopedia by using the wildcard "#"
    client.subscribe("testing", qos=1)

    # a single publish, this can also be done in loops, etc.
    # for i in range(10):
    #     client.publish("testing", payload=str(i), qos=1)

    # loop_forever for simplicity, here you need to stop the loop manually
    # you can also use loop_start and loop_stop
    client.loop_start()
    
    t1 = threading.Thread(target=print_sth_stupid)
    t1.start()
    while(True):
        pass
    
    sys.exit(client.loop_stop())