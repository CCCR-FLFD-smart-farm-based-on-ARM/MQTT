import paho.mqtt.client as mqtt
import json
import time
import random

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)

def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))

def on_publish(client, userdata, mid):
    print("In on_pub callback mid= ", mid)

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.connect('192.168.56.22', 1883)
client.loop_start()

# random한 temperature 데이터 생성
while(True):
    dict1={'temperature':random.uniform(35,40)}
    json_test=json.dumps(dict1)
    client.publish('test2', json_test, 1)
    time.sleep(10)

client.loop_stop()
client.disconnect()
