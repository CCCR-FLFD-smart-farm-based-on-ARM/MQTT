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
    # json file format
    json_body = [
        {
            "measurement": msg.topic,
            "time": receiveTime,
            "fields": msgDict
        }
    ]
    # json file write
    dbclient.write_points(json_body)

# InfluxDB connection(IP, port, ID, password, database name)
dbclient = InfluxDBClient('192.168.100.200', 8086, 'root', 'root1234', 'sensordata')

# MQTT broker connecton
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_message = on_message
# MQTT broker ip, port
client.connect('172.30.1.5', 1883)
# MQTT topic
client.subscribe('temperature', 1)
client.subscribe('humidity', 1)
client.loop_forever()
