# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import numpy
import sqlite3


@blueprint.route('/index')
@login_required
def index():

	try:
		sqliteConnection = sqlite3.connect('/home/neoj/Escritorio/html/material-dashboard-flask-master/apps/db.sqlite3')
		cursor = sqliteConnection.cursor()
		print("Database created and Successfully Connected to SQLite")

		qry = "SELECT * FROM locates;"
		cursor.execute(qry)
		#sqliteConnection.commit()
		record = cursor.fetchall()
		qrySens = "SELECT * FROM sensors;"
		cursor.execute(qrySens)
		sensors = cursor.fetchall()
		
		#Obtener los eventos		
		qryEvents = "SELECT id,id_sensor,id_locate,descripcion,STRFTIME('%d/%m/%Y, %H:%M' ,fecha) as fecha FROM eventos ORDER BY fecha DESC LIMIT(5);"
		cursor.execute(qryEvents)
		events = cursor.fetchall()

		#print("SQLite Database Version is: ", record)
		#lastID = str(cursor.lastrowid)
		cursor.close()

	except sqlite3.Error as error:
		print("Error while connecting to sqlite", error)
	finally:
		if sqliteConnection:
		    sqliteConnection.close()
		    print("The SQLite connection is closed")

	return render_template('home/index.html', segment='index', record=record, sensors=sensors, events=events, page="Inicio")

@blueprint.route('/tables')
@login_required
def tables():
	try:
		sqliteConnection = sqlite3.connect('/home/neoj/Escritorio/html/material-dashboard-flask-master/apps/db.sqlite3')
		cursor = sqliteConnection.cursor()
		print("Database created and Successfully Connected to SQLite")

		#Obtener las ubicaciones
		qry = "SELECT * FROM locates;"
		cursor.execute(qry)
		record = cursor.fetchall()

		#Obtener los sensores
		qrySens = "SELECT * FROM sensors;"
		cursor.execute(qrySens)
		sensors = cursor.fetchall()
		
		
		#print("SQLite Database Version is: ", record)
		#lastID = str(cursor.lastrowid)
		cursor.close()
	except sqlite3.Error as error:
		print("Error while connecting to sqlite", error)
	finally:
		if sqliteConnection:
		    sqliteConnection.close()
		    print("The SQLite connection is closed")		
		    
	return render_template('home/tables.html', segment='tables', record=record, sensors=sensors,page="Configuración")



@blueprint.route('/despensa')
@login_required
def despensa():
	try:
		sqliteConnection = sqlite3.connect('/home/neoj/Escritorio/html/material-dashboard-flask-master/apps/db.sqlite3')
		cursor = sqliteConnection.cursor()
		print("Database created and Successfully Connected to SQLite")

		#Obtener las ubicaciones
		qry = "SELECT * FROM comida;"
		cursor.execute(qry)
		comida = cursor.fetchall()
		cursor.close()
	except sqlite3.Error as error:
		print("Error while connecting to sqlite", error)
	finally:
		if sqliteConnection:
		    sqliteConnection.close()
		    print("The SQLite connection is closed")		
		    
	return render_template('home/despensa.html', segment='billing', comida=comida, page="Despensa")




@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
