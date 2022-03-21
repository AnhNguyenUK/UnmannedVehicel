# This Python file uses the following encoding: utf-8
from concurrent.futures import thread
from queue import Queue
import threading
import re
import os
import sys
import time
from pathlib import Path
from unicodedata import name
from paho import mqtt
import paho.mqtt.client as paho

from PySide2.QtCore import QRunnable, Slot, QThreadPool
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

from mqtt_msg_handler import HiveMqttServer
from dataModel import ElementModel, Manager
# data stack

q = Queue()
dataModel = Manager()        
# setting callbacks for different events to see if it works, print the message etc.
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
    print(str(msg.payload))
    data = msg  
    regex_pattern = r"Id: (.*),.*: (-?\d+.\d+).*: (-?\d+.\d+)"
    data = re.findall(regex_pattern, str(msg.payload))
    q.put(list(data[0]))
    print("Data package: {}".format(data))
    # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_disconnect(client, userdata,rc=0):
    print("DisConnected result code "+str(rc))
    client.loop_stop()

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
    client.on_disconnect = on_disconnect
    client.subscribe("testing", qos=1)
    
    # client.subscribe("testing", qos=1)

def data_handler(manager):
    while(True):
        print("No No No")
        if not q.empty():
            data = q.get()
            print(data)
            manager.addData(data)     

class dataHandlerTask:
    def __init__(self) -> None:
        self.running = True
        
    def terminate(self):
        self.running = False
        
    def exec(self):
        while(self.running):
            # print("No No No")
            if not q.empty():
                data = q.get()
                print(data)
                dataModel.addData(data)

def kill_threads(worker, thread):
    worker.terminate()
    thread.join()

if __name__ == "__main__":
    server_stack = HiveMqttServer()
    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    # thread_list = []
    data_handler_worker = dataHandlerTask()
    data_hander_thread = threading.Thread(target=data_handler_worker.exec, 
                                          name="Data handling thread", 
                                          )
    # client.loop_start()
    connect_init(client)
    client.loop_start()
    data_hander_thread.start()
    app = QGuiApplication(sys.argv)
    app.lastWindowClosed.connect(lambda t_worker = data_handler_worker, 
                                        thread = data_hander_thread: 
                                        kill_threads(t_worker, thread))
    # app.lastWindowClosed.connect(client.loop_stop())
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("dataModel",dataModel)
    engine.load(os.fspath(Path(__file__).resolve().parent / "main.qml"))
    if not engine.rootObjects():
        sys.exit(-1)
        print("Exit")
    # data_hander_thread.join()
    # sys.exit(data_hander_thread.join())
    sys.exit(app.exec_())
    
    # data_hander_thread.join()
    # mqtt_handler_thread.join()
    
