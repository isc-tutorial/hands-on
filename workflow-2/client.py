#!/usr/bin/env python

import os
import platform
import random
import time
from paho.mqtt import client as mqtt_client

broker = os.getenv("BROKER_ADDRESS", "broker.emqx.io")  # Free public MQTT broker
port = int(os.getenv("BROKER_PORT", "1883"))
topic = os.getenv("TOPIC", "data-aggregator")
node = platform.node()

# Generate a Client ID with the subscribe prefix.
client_id = f"client-{random.randint(0, 10000)}"


def on_connect(mqttc, obj, flags, rc):
    print("On connect called")
    mqttc.subscribe(topic)


def on_message(mqttc, obj, msg):
    print(f"Received `{msg.payload.decode()}` from topic `{msg.topic}`")


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from topic `{msg.topic}`")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    client.on_message = on_message
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe

    client.loop_forever()


if __name__ == "__main__":
    run()
