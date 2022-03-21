import os
import sys
import time
import numpy as np
import re
from paho import mqtt
import paho.mqtt.client as paho

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def data_processing():
    # process data msg
    pass
# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    data = msg   
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def connect_init(client):
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

def random_latLng():
    rLat = 90 * np.random.normal(0,0.1,100)
    rLng = 180 * np.random.normal(0,0.1,100)
    return {"Lat":rLat, "Lng":rLng}
    
    
if __name__ == '__main__':
    data = random_latLng()
      
    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    connect_init(client)
    client.loop_start()
    for idx in range(len(data["Lat"])):
        data_frame = "Id: {}, Lat: {}, Lng: {}".format("Dummy",data["Lat"][idx],data["Lng"][idx])
        client.publish("testing", payload=data_frame, qos=1)
        print("Published: {}".format(data_frame))
        time.sleep(3)

    # loop_forever for simplicity, here you need to stop the loop manually
    # you can also use loop_start and loop_stop
    client.loop_stop()
    # print((data["Lat"] < 90) & (data["Lat"]>-90))
    # regex_pattern = r"Id: (.*),.*: (-?\d+.\d+).*: (-?\d+.\d+)"
    # for i in range(len(data["Lat"])):
    #     data_frame = "Id: {}, Lat: {}, Lng: {}".format("Dummy",data["Lat"][i],data["Lng"][i])
    #     print(data_frame)
    #     print(re.findall(regex_pattern,data_frame))
    
