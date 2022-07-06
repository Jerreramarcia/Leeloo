#!/bin/bash

#"Ti sensor" $1 
#"ID sensor" $2
#"ID locate" $3

#Añadir unsafe_install para pode instalar librerias desde github o zip's
set ARDUINO_LIBRARY_ENABLE_UNSAFE_INSTALL=true
#importar la libreria mosquitto
sudo ./apps/arduino-cli lib install PubSubClient
#importar la libreria de DHT11
sudo ./apps/arduino-cli lib install "Adafruit Unified Sensor"
sudo ./arduino-cli lib install --git-url https://github.com/adafruit/DHT-sensor-library

#generar codigo
sudo ./apps/ESP$1.sh $2 $3
#compilar codigo
sudo ./apps/arduino-cli compile --fqbn esp8266:esp8266:generic apps/ESP$1
#subir codigo
sudo ./apps/arduino-cli upload -p /dev/ttyUSB0 --fqbn esp8266:esp8266:generic apps/ESP$1
