# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users
from werkzeug.utils import secure_filename
from apps.authentication.util import verify_pass
import sqlite3
#Usamos para crear comandos en bash
import subprocess
import tensorflow as tf
import os
import numpy as np


def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(os.path.join(basedir, 'db.sqlite3'))
    except Error as e:
        print(e)

    return conn

@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))

@blueprint.route('/renameLocation',methods=['POST'])
def renameLocation():
	try:
		sqliteConnection = sqlite3.connect('/home/neoj/Escritorio/html/material-dashboard-flask-master/apps/db.sqlite3')
		cursor = sqliteConnection.cursor()

		qry = "UPDATE locates set descripcion= '"+ request.form['rename'] +"' WHERE id = "+ request.form['id'] +";"
		cursor.execute(qry)
		sqliteConnection.commit()
		cursor.close()

	except sqlite3.Error as error:
		print("Error while connecting to sqlite", error)
	finally:
		if sqliteConnection:
		    sqliteConnection.close()
		    print("The SQLite connection is closed")

	return(qry)


@blueprint.route('/renameSensor',methods=['POST'])
def renameSensor():
	try:
		sqliteConnection = sqlite3.connect('/home/neoj/Escritorio/html/material-dashboard-flask-master/apps/db.sqlite3')
		cursor = sqliteConnection.cursor()

		qry = "UPDATE sensors set descripcion = '"+ request.form['rename'] +"' WHERE id = "+ request.form['id'] +";"
		cursor.execute(qry)
		sqliteConnection.commit()
		cursor.close()

	except sqlite3.Error as error:
		print("Error while connecting to sqlite", error)
	finally:
		if sqliteConnection:
		    sqliteConnection.close()
		    print("The SQLite connection is closed")

	return(qry)




@blueprint.route('/configSensor',methods=['POST'])
def configSensor():
	#comando, parametro
			#Obtener los sensores
	sqliteConnection = sqlite3.connect('/home/neoj/Escritorio/html/material-dashboard-flask-master/apps/db.sqlite3')
	cursor = sqliteConnection.cursor()

	qrySens = "SELECT * FROM sensors WHERE id = "+request.form['idSensor']
	cursor.execute(qrySens)
	sensors = cursor.fetchall()
	#Obtener informacion del sensor
	tipo = str(sensors[0][2])
	idSensor = str(sensors[0][0])
	idLocate = str(sensors[0][3])
	
	#Ejecutar los comandos necesarios para subir el código y generarlo
	bashCmd = ["./apps/compile.sh", tipo, idLocate, idSensor]
	process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
	output, error = process.communicate()
	salida = str(output)
	if "Hard resetting via RTS pin..." in salida:
		#Si todo sale bien, ponemos el estado del sensor a 1
		qrySensON = "UPDATE sensors set activado = 1 WHERE id = "+ request.form['idSensor'] +";"
		cursor.execute(qrySensON)
		sqliteConnection.commit()
		cursor.close()
		return(qrySensON)
	return("error")




@blueprint.route('/configCam',methods=['POST'])
def configCam():
	#comando, parametro
			#Obtener los sensores
	sqliteConnection = sqlite3.connect('/home/neoj/Escritorio/html/material-dashboard-flask-master/apps/db.sqlite3')
	cursor = sqliteConnection.cursor()

#	qrySens = "SELECT * FROM sensors WHERE id = "+request.form['idSensor']
#	cursor.execute(qrySens)
#	sensors = cursor.fetchall()
	#Obtener informacion del sensor
#	tipo = str(sensors[0][2])
#	idSensor = str(sensors[0][0])
#	idLocate = str(sensors[0][3])
#	Ejecutar los comandos necesarios para subir el código y generarlo
	bashCmd = ["./apps/ping.sh", str(request.form['urlCam'])]
	process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
	output, error = process.communicate()
	salida = str(output)
	if "3 received" in salida:
		#Si todo sale bien, ponemos el estado del sensor a 1
		qryCamActivate = "UPDATE sensors set activado = 1 WHERE id = "+ request.form['id'] +";"
		qrySensON = "UPDATE sensors set IP = '"+str(request.form['urlCam'])+"' WHERE id = "+ request.form['id'] +";"
		cursor.execute(qryCamActivate)
		cursor.execute(qrySensON)
		sqliteConnection.commit()
		cursor.close()
		return("ok")
	return("error")




@blueprint.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        model = tf.keras.models.load_model("apps/model.h5")
        f = request.files['file']
        f.save(os.path.join("apps/predict/", secure_filename(f.filename)))
        img_path = os.path.join("apps/predict/", secure_filename(f.filename))
        img = tf.keras.utils.load_img(
            img_path, target_size=(224, 224)
        )
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)
        predictions = model.predict(img_array)
        class_names = ['Apple', 'Banana', 'Tomato' ,'Watermelon']

        try:
            sqliteConnection = sqlite3.connect(
                '/home/neoj/Escritorio/html/material-dashboard-flask-master/apps/db.sqlite3')
            cursor = sqliteConnection.cursor()
            
            getFood = "SELECT id FROM comida WHERE nombre = '"+str(format(class_names[np.argmax(predictions)]))+"';";
            cursor.execute(getFood)
            idFood = cursor.fetchall()
            if(idFood):
                updateFood = "UPDATE comida SET cantidad= cantidad+1 WHERE nombre = '" + str(format(class_names[np.argmax(predictions)])) +"';"
                cursor.execute(updateFood)
                sqliteConnection.commit()
            else:
                insertFood = "INSERT INTO comida ('nombre','cantidad') VALUES('" + str(format(class_names[np.argmax(predictions)])) +"'," + str(1) + ");"
                cursor.execute(insertFood)
                sqliteConnection.commit()
                return redirect("despensa/") 
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("The SQLite connection is closed")
    return redirect("despensa") 


@blueprint.route('/deleteFood',methods=['POST'])
def deleteFood():
	try:
		sqliteConnection = sqlite3.connect('/home/neoj/Escritorio/html/material-dashboard-flask-master/apps/db.sqlite3')
		cursor = sqliteConnection.cursor()

		delSensor = "DELETE FROM comida WHERE id = "+ request.form['id'] +";"
		cursor.execute(delSensor)
		sqliteConnection.commit()
		cursor.close()

	except sqlite3.Error as error:
		print("Error while connecting to sqlite", error)
	finally:
		if sqliteConnection:
		    sqliteConnection.close()
		    print("The SQLite connection is closed")

	return("")



@blueprint.route('/useFood',methods=['POST'])
def useFood():
    try:
        sqliteConnection = sqlite3.connect('/home/neoj/Escritorio/html/material-dashboard-flask-master/apps/db.sqlite3')
        cursor = sqliteConnection.cursor()
        useFood = "UPDATE comida SET cantidad= cantidad-1 WHERE id = " + request.form['id'] +";"
        cursor.execute(useFood)
        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

    return("")


@blueprint.route('/addFood',methods=['POST'])
def addFood():
	try:
		sqliteConnection = sqlite3.connect('/home/neoj/Escritorio/html/material-dashboard-flask-master/apps/db.sqlite3')
		cursor = sqliteConnection.cursor()
		useFood = "UPDATE comida SET cantidad= cantidad+1 WHERE id = " + request.form['id'] +";"
		cursor.execute(useFood)
		sqliteConnection.commit()
		cursor.close()

	except sqlite3.Error as error:
		print("Error while connecting to sqlite", error)
	finally:
		if sqliteConnection:
		    sqliteConnection.close()
		    print("The SQLite connection is closed")

	return("")



@blueprint.route('/renameSensorType',methods=['POST'])
def renameSensorType():
	try:
		sqliteConnection = sqlite3.connect('/home/neoj/Escritorio/html/material-dashboard-flask-master/apps/db.sqlite3')
		cursor = sqliteConnection.cursor()

		renameTypeSensor = "UPDATE sensors set tipo = "+ request.form['rename'] +" WHERE id = "+ request.form['id'] +";"
		cursor.execute(renameTypeSensor)
		sqliteConnection.commit()
		cursor.close()

	except sqlite3.Error as error:
		print("Error while connecting to sqlite", error)
	finally:
		if sqliteConnection:
		    sqliteConnection.close()
		    print("The SQLite connection is closed")

	return(renameTypeSensor)

@blueprint.route('/deleteSensor',methods=['POST'])
def deleteSensor():
	try:
		sqliteConnection = sqlite3.connect('/home/neoj/Escritorio/html/material-dashboard-flask-master/apps/db.sqlite3')
		cursor = sqliteConnection.cursor()

		delSensor = "DELETE FROM sensors WHERE id = "+ request.form['id'] +";"
		cursor.execute(delSensor)
		sqliteConnection.commit()
		cursor.close()

	except sqlite3.Error as error:
		print("Error while connecting to sqlite", error)
	finally:
		if sqliteConnection:
		    sqliteConnection.close()
		    print("The SQLite connection is closed")

	return(qry)
	
@blueprint.route('/deleteLocate',methods=['POST'])
def deleteLocate():
	try:
		sqliteConnection = sqlite3.connect('/home/neoj/Escritorio/html/material-dashboard-flask-master/apps/db.sqlite3')
		cursor = sqliteConnection.cursor()

		delLocate = "DELETE FROM locates WHERE id = "+ request.form['id'] +";"
		cursor.execute(delLocate)
		sqliteConnection.commit()
		
		delSensors = "DELETE FROM sensors WHERE locate = "+ request.form['id'] +";"
		cursor.execute(delSensors)
		sqliteConnection.commit()
		
		cursor.close()
		

	except sqlite3.Error as error:
		print("Error while connecting to sqlite", error)
	finally:
		if sqliteConnection:
		    sqliteConnection.close()
		    print("The SQLite connection is closed")

	return(qry)


@blueprint.route('/ubicacionAdd',methods=['GET', 'POST'])
def ubicaionAdd():
	try:
		sqliteConnection = sqlite3.connect('/home/neoj/Escritorio/html/material-dashboard-flask-master/apps/db.sqlite3')
		cursor = sqliteConnection.cursor()
		print("Database created and Successfully Connected to SQLite")

		qry = "INSERT INTO locates (descripcion,inserted) VALUES ('',1);"
		cursor.execute(qry)
		sqliteConnection.commit()
		#record = cursor.fetchall()
		#print("SQLite Database Version is: ", record)
		lastID = str(cursor.lastrowid)
		cursor.close()
		return(lastID)

	except sqlite3.Error as error:
		print("Error while connecting to sqlite", error)
	finally:
		if sqliteConnection:
		    sqliteConnection.close()
		    print("The SQLite connection is closed")

	print ("Hello")
	return (qry)
	

@blueprint.route('/sensorLocation',methods=['GET', 'POST'])
def sensorLocation():
	try:
		sqliteConnection = sqlite3.connect('/home/neoj/Escritorio/html/material-dashboard-flask-master/apps/db.sqlite3')
		cursor = sqliteConnection.cursor()
		print("Database created and Successfully Connected to SQLite")

		qry = "INSERT INTO sensors (descripcion,locate,activado) VALUES ('',"+request.form['id']+",0);"
		cursor.execute(qry)
		sqliteConnection.commit()
		#record = cursor.fetchall()
		#print("SQLite Database Version is: ", record)
		lastID = str(cursor.lastrowid)
		cursor.close()
		return(lastID)

	except sqlite3.Error as error:
		print("Error while connecting to sqlite", error)
	finally:
		if sqliteConnection:
		    sqliteConnection.close()
		    print("The SQLite connection is closed")

	print ("Hello")
	return (qry)


# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template('accounts/register.html',
                               msg='User created please <a href="/login">login</a>',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
