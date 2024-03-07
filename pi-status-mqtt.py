#!/usr/bin/python3
#-----------------------------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
# Project : Pi CPU Temperature MQTT Publish
# File    : pi_temp_mqtt_publish.py
#
# Script to send the Pi CPU temperature to MQTT broker.
#
# Author : Matt Hawkins
# Date   : 06/03/2024
# Source : https://github.com/RPiSpy/pi-status-mqtt/
#
# Install instructions here:
# https://www.raspberrypi-spy.co.uk/
#
# gpiozero CPUTemperature reference:
# https://gpiozero.readthedocs.io/en/stable/api_internal.html?#cputemperature
#
#-----------------------------------------------------------
import paho.mqtt.client as mqtt
import gpiozero as gz
import time

import config as c

def on_connect(client, userdata, flags, reason_code, properties):
  if reason_code==0:
    print(f"Connected with result code {reason_code}")
  if reason_code>0:
    print(f"Error connecting with reason code {reason_code}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username=c.MQTT_USER,password=c.MQTT_PASSWORD)
client.on_connect = on_connect
client.connect(c.MQTT_SERVER, c.MQTT_PORT, 60)

# Get Pi CPU Temperature
cpu = gz.CPUTemperature()
cpu_temp = cpu.temperature
cpu_temp = round(cpu_temp, 1)

# Publish to MQTT broker
result=client.publish(c.MQTT_TOPIC_TEMP, payload=cpu_temp, qos=0, retain=False)
if result.rc==mqtt.MQTT_ERR_SUCCESS:
  print(f"Successfully sent {cpu_temp} to {c.MQTT_TOPIC_TEMP}")
else:
  print("Error publishing message")

# Get Pi Disk Usage
disk = gz.DiskUsage()
disk_usage = disk.usage
disk_usage = round(disk_usage, 1)

# Publish to MQTT broker
result=client.publish(c.MQTT_TOPIC_DISK, payload=disk_usage, qos=0, retain=False)
if result.rc==mqtt.MQTT_ERR_SUCCESS:
  print(f"Successfully sent {disk_usage} to {c.MQTT_TOPIC_DISK}")
else:
  print("Error publishing message")


client.disconnect()
