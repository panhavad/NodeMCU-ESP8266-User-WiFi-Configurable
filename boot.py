try:
  import usocket as socket
except:
  import socket
from machine import Pin, PWM
import utime, ujson, network, urequests, json, esp, gc, ure

#defualt code for ESP8266 to work normally
esp.osdebug(None) 
gc.collect()
BUILTIN_LED = 2
RESET_PIN = 16 

#read configured setting
with open("config","r") as file:
  ssid = file.read()
  
password = ''#TODO

#obj adapter
station = network.WLAN(network.STA_IF)
wifiap = network.WLAN(network.AP_IF)

#activate the AP Mode & Wifi Mode
wifiap.active(True)
station.active(True)

#enable socket connection
prime_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
prime_socket.bind(('0.0.0.0', 80))
prime_socket.settimeout(3)#session timeout
prime_socket.listen(5)

#AP Mode configuration
wifiap.config(essid="CONFIG_ME", password="iwanttoconfigureyounow")#TODO
station.connect(ssid, password)#Connect to the network

led_pin = Pin(BUILTIN_LED, Pin.OUT)
reset = Pin(RESET_PIN, Pin.OUT)

wifi_list = []