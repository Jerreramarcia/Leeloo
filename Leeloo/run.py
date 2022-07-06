# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_migrate import Migrate
from sys import exit
from decouple import config
from apps.config import config_dict
from apps import create_app, db
import sqlite3

"""
Parte 1
"""
import logging
from flask import Flask, request, render_template
from flask_socketio import SocketIO, send, emit                                      # (1)
#from gpiozero import PWMLED, Device
#from gpiozero.pins.pigpio import PiGPIOFactory
from flask import Flask, render_template, request
from flask_mqtt import Mqtt
import eventlet
import json
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap


eventlet.monkey_patch()

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')
app = create_app(app_config)

app.config.update(
	#MQTT_BROKER_URL = '192.168.1.62',  # use the free broker from HIVEMQ
	MQTT_BROKER_URL = '192.168.0.99',
	MQTT_BROKER_PORT = 1883,  # default port for non-tls connection
	MQTT_KEEPALIVE = 5,  # set the time interval for sending a ping to the broker to 5 seconds
	UPLOAD_FOLDER = "/home/neoj/Escritorio/html/material-dashboard-flask-master/apps/predict/"
)
socketio = SocketIO(app) # Flask-SocketIO extension wrapper.                         # (2)
mqtt = Mqtt(app)

Migrate(app, db)



"""LED CONTROL"""

@socketio.on('led')
def offalice(data, sensor,locate):
	sqliteConnection = sqlite3.connect('/home/neoj/Escritorio/html/material-dashboard-flask-master/apps/db.sqlite3')
	cursor = sqliteConnection.cursor()
	
	locateQRY = "SELECT descripcion FROM locates WHERE id = '"+str(locate)+"'";
	cursor.execute(locateQRY)
	locateName = cursor.fetchall()	
	locate2 = locateName[0][0]
	print(data)
	if data == 1:
		mqtt.publish('casa/'+str(sensor)+'/'+str(sensor), '1')
		qry = "INSERT INTO eventos (id_sensor,id_locate,descripcion) VALUES ("+str(sensor)+","+str(locate)+",'Led encendido ("+locate2+")');"
		print(qry)
		cursor.execute(qry)
		sqliteConnection.commit()
	else:
		mqtt.publish('casa/'+str(sensor)+'/'+str(sensor), '0')
		qry = "INSERT INTO eventos (id_sensor,id_locate,descripcion) VALUES ("+str(sensor)+","+str(locate)+",'Led apagado ("+locate2+")');"
		print(qry)
		cursor.execute(qry)
		sqliteConnection.commit()
	cursor.close()

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('casa/#')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    if "_" in message.payload.decode():
	    socketio.emit('temp', data=data)



"""
Fin pruebas
"""

from flask_cors import CORS
CORS(app)


if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG))
    app.logger.info('Environment = ' + get_config_mode)
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info('MQTT_BROKER_URL = '+ app.config["MQTT_BROKER_URL"])

if __name__ == "__main__":
    socketio.run(app, debug=True,host='192.168.0.239')                                    # (14)
