# SPDX-FileCopyrightText: 2023 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import json
import time
from os import getenv

import adafruit_connection_manager
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import wifi

from adafruit_aws_iot import MQTT_CLIENT

# Add a settings.toml to your filesystem. DO NOT share that file or commit it into
# Git or other source control. The file should have the following settings:
"""
CIRCUITPY_WIFI_SSID="Your WiFi ssid"
CIRCUITPY_WIFI_PASSWORD="Your WiFi password"
device_cert_path="<THING_NAME>.cert.pem"  # Path to the Device Certificate from AWS IoT
device_key_path="<THING_NAME>.private.key"  # Path to the RSA Private Key from AWS IoT
broker="<PREFIX>.iot.<REGION>.amazonaws.com"  # The endpoint for the AWS IoT broker
client_id="client_id"  # The client id. Your device's Policy needs to allow this client
"""

# Get WiFi details and AWS keys, ensure these are setup in settings.toml
ssid = getenv("CIRCUITPY_WIFI_SSID")
password = getenv("CIRCUITPY_WIFI_PASSWORD")
device_cert_path = getenv("device_cert_path")
device_key_path = getenv("device_key_path")
broker = getenv("broker")
client_id = getenv("client_id")

### Code ###

# Your device's Policy needs to allow this topic
topic = "sdk/test/python"


# Define callback methods which are called when events occur
def connect(client, userdata, flags, rc):
    # This function will be called when the client is connected
    # successfully to the broker.
    print("Connected to MQTT Broker!")
    print(f"Flags: {flags} - RC: {rc}")

    # Subscribe to topic circuitpython/aws
    print(f"Subscribing to topic {topic}")
    aws_iot.subscribe(topic)


def disconnect(client, userdata, rc):
    # This method is called when the client disconnects
    # from the broker.
    print("Disconnected from MQTT Broker!")


def subscribe(client, userdata, topic, granted_qos):
    # This method is called when the client subscribes to a new topic.
    print(f"Subscribed to {topic} with QOS level {granted_qos}")

    # Create a json-formatted message
    message = {"message": "Hello from AWS IoT CircuitPython"}
    # Publish message to topic
    aws_iot.publish(topic, json.dumps(message))


def unsubscribe(client, userdata, topic, pid):
    # This method is called when the client unsubscribes from a topic.
    print(f"Unsubscribed from {topic} with PID {pid}")


def publish(client, userdata, topic, pid):
    # This method is called when the client publishes data to a topic.
    print(f"Published to {topic} with PID {pid}")


def message(client, topic, msg):
    # This method is called when the client receives data from a topic.
    print(f"Message from {topic}: {msg}")


print(f"Connecting to {ssid}")
wifi.radio.connect(ssid, password)
print(f"Connected to {ssid}!")

# Create a socket pool
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)

# Set AWS Device Certificate and AWS RSA Private Key
ssl_context.load_cert_chain(certfile=device_cert_path, keyfile=device_key_path)

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker=broker,
    client_id=client_id,
    is_ssl=True,
    socket_pool=pool,
    ssl_context=ssl_context,
)

# Initialize AWS IoT MQTT API Client
aws_iot = MQTT_CLIENT(mqtt_client)

# Connect callback handlers to AWS IoT MQTT Client
aws_iot.on_connect = connect
aws_iot.on_disconnect = disconnect
aws_iot.on_subscribe = subscribe
aws_iot.on_unsubscribe = unsubscribe
aws_iot.on_publish = publish
aws_iot.on_message = message

print(f"Attempting to connect to {mqtt_client.broker}")
aws_iot.connect()

# Start a blocking message loop...
# NOTE: NO code below this loop will execute
# NOTE: Network reconnection is NOT handled within this loop
while True:
    aws_iot.loop(10)

    time.sleep(1)
