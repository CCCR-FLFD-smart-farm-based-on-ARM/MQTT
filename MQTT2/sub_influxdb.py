import paho.mqtt.client as mqtt
import datetime
import time
import json
from influxdb import InfluxDBClient

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)

def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))

def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    receiveTime=datetime.datetime.utcnow()
    message=msg.payload.decode("utf-8")

    print(str(receiveTime) + ": " + msg.topic + " payload : " + str(msg.payload))
    msgDict = json.loads(msg.payload)

    json_body = [
        {
            "measurement": msg.topic,
            "time": receiveTime,
            "fields": msgDict
        }
    ]

    dbclient.write_points(json_body)

dbclient = InfluxDBClient('192.168.56.22', 8086, 'root', 'root', 'sensordata')

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect('192.168.56.22', 1883)
client.subscribe('test2', 1)
client.loop_forever()
