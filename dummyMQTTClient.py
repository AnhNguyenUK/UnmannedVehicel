import os
import sys
from urllib import response
import serial
import numpy as np
import re
import math
import threading
import subprocess
from time import sleep
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

def input_handler(serial, lock):
    lock.acquire()
    while True:
        text = input('Send AT: ')
        serial.write(text.encode('utf-8'))
        sleep(0.5)
        while serial.in_waiting > 0:
            line = serial.readline().decode('utf-8')
            print("Response: ",line)
    lock.release() 

def response_handler(serial, lock):
    lock.acquire()
    while True:
        if serial.in_waiting > 0:
            line = serial.read(100).decode('utf-8').rstrip()
            print("Response: ",line)
    lock.release()

def sendATcommands(cmd, serial):
    response = cmd
    while (response == cmd): 
        serial.write(('{}\r'.format(cmd)).encode('utf-8'))
        sleep(1)
        response = serial.read(100).decode('utf-8').replace(' ','')
        response = str(response).replace(cmd,'')
        response = str(response).replace('\r','')
        response = str(response).replace('\n','')
    print('{}: {}'.format(cmd, response))
    sleep(1)

def sendATCommendsThroughChatScripts(cmd):
    numOfRepeat = 3
    response = ""
    for i in range(numOfRepeat):
        response = str(subprocess.run("chat -V -s '' '{}' 'OK' '' > /dev/ttyS0 < /dev/ttyS0".format(cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE))    
    print(response)

def getGPS(debug=True):
    num_of_repeat = 5
    gps_data_pattern = ".*CGPSINFO: (.*),([N|S]),(.*),([W|E]),.*"
    for i in range(num_of_repeat):
        a = str(subprocess.run("chat -V -s '' 'AT+CGPSINFO' 'OK' '' > /dev/ttyS0 < /dev/ttyS0",
                                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
    if debug == True:
        print(a)
    data = re.findall(gps_data_pattern,str(a))
    if debug == True:
        print(data)
    latti = float(data[0][0])
    longi = float(data[0][2])
    sign_latti = 1
    if data[0][1]=='S':
        sign_latti = -1
    sign_longi = 1
    if data[0][3]=='W':
        sign_longi = -1
    if debug == True:
        print([latti, longi])
        print([sign_latti, sign_longi])
    latti = (math.floor(latti)//100 + (round(latti,2)%100)/60) * sign_latti
    longi = (math.floor(longi)//100 + (round(longi,2)%100)/60) * sign_longi
    return {"Lat":latti, "Lng":longi}
    
if __name__ == '__main__':
    
    ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)

    sendATcommands('AT+CGPS=0',ser)
    sendATcommands('AT+CGPSNMEA=71',ser)
    sendATcommands('AT+CGPS=1', ser)
    sendATcommands('AT+CGPSINFO',ser)
    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    connect_init(client)
    client.loop_start()
    # for idx in range(len(data["Lat"])):
    while(1):
        data = getGPS(debug=False)
        data_frame = "Id: {}, Lat: {}, Lng: {}".format("Dummy",data["Lat"],data["Lng"])
        client.publish("testing", payload=data_frame, qos=1)
        print("Published: {}".format(data_frame))
        sleep(3)

    # loop_forever for simplicity, here you need to stop the loop manually
    # you can also use loop_start and loop_stop
    client.loop_stop()

    
