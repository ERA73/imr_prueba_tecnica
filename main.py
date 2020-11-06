import os
import traceback
import base64
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from datetime import datetime
from dao import *
import app_config_parameters as acp



app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = acp.TEMPLATES_AUTO_RELOAD

# MySQL connection
app.config['MYSQL_HOST'] = acp.MYSQL_HOST
app.config['MYSQL_USER'] = acp.MYSQL_USER
app.config['MYSQL_PASSWORD'] = acp.MYSQL_PASSWORD
app.config['MYSQL_DB'] = acp.MYSQL_DB
mysql = MySQL(app)

# Archivos
app.config['UPLOAD_FOLDER'] = acp.UPLOAD_FOLDER

#settings
app.secret_key = acp.secret_key

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in acp.ALLOWED_EXTENSIONS

@app.route('/')
def defaul():
	try:
		return render_template("index.html")
	except:
		traceback.print_exc()
		flash('Error inesperado, sentimos las molestias')
		return render_template("index.html")

@app.route('/index')
def index():
	try:
		return redirect(url_for('defaul'))
	except:
		traceback.print_exc()
		flash('Error inesperado, sentimos las molestias')
		return redirect(url_for('defaul'))

@app.route('/enrutar', methods = ['POST'])
def enrutar():
	try:
		if request.method == 'POST':
			print(request.form)
			if "crear_usuario" in request.form.keys():
				return redirect(url_for('crear_usuario_form'))
			elif "registrar_vehiculo" in request.form.keys():
				return redirect(url_for('registrar_vehiculo_form'))
			elif "entrada_parqueadero" in request.form.keys():
				return redirect(url_for('entrada_parqueadero_form'))
			elif "informes" in request.form.keys():
				return redirect(url_for('informes_form'))
	except:
		traceback.print_exc()
		flash('Error inesperado, sentimos las molestias')
		return redirect(url_for('defaul'))

@app.route('/crear_usuario_form')
def crear_usuario_form():
	try:
		cur = mysql.connection.cursor()
		cur.execute('SELECT * FROM usuario')
		data = cur.fetchall()
		return render_template("crear_usuario.html", usuarios = data)
	except:
		traceback.print_exc()
		flash('Error inesperado, sentimos las molestias')
		return redirect(url_for('defaul'))

@app.route('/registrar_vehiculo_form')
def registrar_vehiculo_form():
	try:
		return render_template("registrar_vehiculo.html", placa_vehiculo = "", check_carro = "", check_moto = "", check_bicicleta = "checked")
	except:
		traceback.print_exc()
		flash('Error inesperado, sentimos las molestias')
		return redirect(url_for('defaul'))

@app.route('/entrada_parqueadero_form')
def entrada_parqueadero_form():
	try:
		return render_template("entrada_parqueadero.html")
	except:
		traceback.print_exc()
		flash('Error inesperado, sentimos las molestias')
		return redirect(url_for('defaul'))

def get_months():
	months = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
	months = [m.capitalize() for m in months]
	return months

def get_fecha():
	today = datetime.today()
	years = [2000, today.year]
	months = get_months()
	current = [today.year, months[today.month-1]]
	return [years, months, current]

@app.route('/informes_form')
def informes_form():
	try:
		fecha = get_fecha()
		return render_template("informes.html", years = fecha[0], months = fecha[1], current = fecha[2])
	except:
		traceback.print_exc()
		flash('Error inesperado, sentimos las molestias')
		return redirect(url_for('defaul'))

def get_documentos(documento = ""):
	try:
		filtro_documento = "" if documento == "" else "AND documento = {}".format(documento)
		cur = mysql.connection.cursor()
		cur.execute("""
		SELECT * FROM usuario 
		WHERE documento IN 
		(SELECT us_documento FROM carro
		UNION
		SELECT us_documento FROM moto
		UNION
		SELECT us_documento FROM bicicleta)
		{}
		""".format(filtro_documento))
		documentos = list(cur.fetchall())
		return documentos
	except:
		return []

@app.route('/generar_informe', methods = ['POST'])
def generar_informe():
	try:
		if request.method == 'POST':
			consultas = dao()
			fecha = get_fecha()
			documento = request.form['documento']
			year = request.form['year']
			month = request.form['month']
			current = [year, get_months()[int(month)-1]]
			if year == "":
				flash('Debe escribir un año')
				return redirect(url_for('informes_form'))
			if documento == "":
				documentos = get_documentos()
			else:
				documentos = get_documentos(documento)
			cur = mysql.connection.cursor()
			data_info = []
			for doc in documentos:
				cur.execute(consultas.get_consulta_parqueo_carro(year, month, doc[0]))
				data_carro = list(cur.fetchall())
				print(data_carro)
				data_carro = len(data_carro)
				cur.execute(consultas.get_consulta_parqueo_moto(year, month, doc[0]))
				data_moto = list(cur.fetchall())
				print(data_moto)
				data_moto = len(data_moto)
				cur.execute(consultas.get_consulta_parqueo_bicicleta(year, month, doc[0]))
				data_bicicleta = list(cur.fetchall())
				print(data_bicicleta)
				data_bicicleta = len(data_bicicleta)
				cur.execute(consultas.get_consulta_parqueo_total(year, month, doc[0]))
				data_total = list(cur.fetchall())
				data_total = len(data_total)

				if data_total == 0:
					continue
				nombre = "{} {}".format(doc[1], doc[2])
				data_info.append([doc[0], nombre, data_carro, data_moto, data_bicicleta, data_total])
			if len(data_info) == 0:
				flash('No hay resultados para mostrar')
			return render_template("informes.html", years = fecha[0], months = fecha[1], data_info = data_info, current = current)
	except:
		traceback.print_exc()
		flash('Error inesperado, sentimos las molestias')
		return redirect(url_for('defaul'))

@app.route('/crear_usuario', methods = ['POST'])
def crear_usuario():
	try:
		if request.method == 'POST':
			documento = request.form['documento']
			nombres = request.form['nombres']
			apellidos = request.form['apellidos']
			if documento == "" or nombres == "" or apellidos == "":
				flash('Debe llenar todos los campos')
				return redirect(url_for('crear_usuario_form'))
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO usuario (documento, nombres, apellidos) VALUES ({},\"{}\",\"{}\")".format(documento, nombres, apellidos))
			mysql.connection.commit()
			flash('Contacto agregado correctamente')
			return redirect(url_for('crear_usuario_form'))
	except:
		traceback.print_exc()
		flash('Error inesperado, sentimos las molestias')
		return redirect(url_for('defaul'))

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in acp.ALLOWED_EXTENSIONS

@app.route('/registrar_vehiculo', methods = ['GET','POST'])
def registrar_vehiculo():
	try:
		if request.method == 'POST':
			documento = request.form['documento']
			option = request.form['rb_vehiculo']
			
			if documento == "":
				flash('Debe escribir el documento')
				return redirect(url_for('registrar_vehiculo_form'))

			#if 'foto' not in request.files:
			#	flash('no se puede cargar el archibo')
			#	return redirect(request.url)
			foto = request.files['foto']
			if foto.filename == '':
				foto = ""
			if foto and allowed_file(foto.filename):
				filename = secure_filename(foto.filename)
				print("my_path")
				print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				foto = filename
				print("filename:")
			print(len(foto))
			cur = mysql.connection.cursor()
			if option == "carro":
				placa_carro = request.form['placa_carro']
				modelo = request.form['modelo']
				puertas = request.form['puertas']
				if placa_carro == "" or modelo == "" or puertas == "":
					flash('Debe completar los datos del carro')
					return render_template("registrar_vehiculo.html", placa_vehiculo = "", check_carro = "checked", check_moto = "", check_bicicleta = "")
				cur.execute("INSERT INTO carro (placa, modelo, puertas, foto, us_documento) VALUES (\"{}\",\"{}\",{},\"{}\",{})".format(placa_carro, modelo, puertas, foto, documento))
				mysql.connection.commit()
				flash('Carro agregado correctamente')
			elif option == "moto":
				placa_moto = request.form['placa_moto']
				cilindraje = request.form['cilindraje']
				tiempos = request.form['tiempos']
				if placa_moto == "" or cilindraje == "" or tiempos == "":
					flash('Debe completar los datos de la moto')
					return render_template("registrar_vehiculo.html", placa_vehiculo = "", check_carro = "", check_moto = "checked", check_bicicleta = "")
				cur.execute("INSERT INTO moto (placa, cilindraje, tiempos, foto, us_documento) VALUES (\"{}\",\"{}\",\"{}\",\"{}\",{})".format(placa_moto, cilindraje, tiempos, foto, documento))
				mysql.connection.commit()
				flash('Moto agregada correctamente')
			else:
				cur.execute("INSERT INTO bicicleta (foto, us_documento) VALUES (\"{}\",{})".format(foto, documento))
				mysql.connection.commit()
				flash('Bicicleta agregada correctamente')
			return redirect(url_for('registrar_vehiculo_form'))
	except:
		traceback.print_exc()
		flash('Error inesperado, sentimos las molestias')
		return redirect(url_for('defaul'))

@app.route('/buscar_usuario', methods = ['POST'])
def buscar_usuario():
	try:
		if request.method == 'POST':
			cur = mysql.connection.cursor()
			if "buscar_usuario" in request.form.keys():
				documento = request.form['documento']
				if documento == "":
					flash('Debe escribir el documento')
					return redirect(url_for("entrada_parqueadero_form"))
				#obtener carros del usuario
				cur.execute('SELECT * FROM carro WHERE us_documento = {}'.format(documento))
				data_carros = cur.fetchall()
				ingreso_carros = []
				for data_carro in data_carros:
					ingreso_carros.append(datos_parqueadero("carro", data_carro[0]))
				#obtener motos del usuario
				cur.execute('SELECT * FROM moto WHERE us_documento = {}'.format(documento))
				data_motos = cur.fetchall()
				ingreso_motos = []
				for data_moto in data_motos:
					ingreso_motos.append(datos_parqueadero("moto", data_moto[0]))
				#obtener bicicletas del usuario
				cur.execute('SELECT * FROM bicicleta WHERE us_documento = {}'.format(documento))
				data_bicicletas = cur.fetchall()
				ingreso_bicicletas = []
				for data_bicicleta in data_bicicletas:
					ingreso_bicicletas.append(datos_parqueadero("bicicleta", data_bicicleta[0]))
				"""print(data_bicicletas)
				for data_bicicleta in data_bicicletas:
					print(data_bicicleta)
					data_bicicleta[1] = "" if data_bicicleta[1] == "" else url_for('uploads/', filename=data_bicicleta[1])"""
				

				return render_template("entrada_parqueadero.html", usuario_carros = [data_carros, ingreso_carros], usuario_motos = [data_motos, ingreso_motos], usuario_bicicletas = [data_bicicletas, ingreso_bicicletas])
	except:
		traceback.print_exc()
		flash('Error inesperado, sentimos las molestias')
		return redirect(url_for('defaul'))

@app.route('/buscar_vehiculo', methods = ['POST'])
def buscar_vehiculo():
	try:
		if request.method == 'POST':
			cur = mysql.connection.cursor()
			if "buscar_vehiculo" in request.form.keys():
				placa = request.form['placa']
				if placa == "":
					flash('Debe escribir una placa')
					return redirect(url_for("entrada_parqueadero_form"))
				#obtener carros del usuario
				cur.execute('SELECT * FROM carro WHERE placa = \"{}\"'.format(placa))
				data_carros = cur.fetchall()
				ingreso_carros = []
				for data_carro in data_carros:
					ingreso_carros.append(datos_parqueadero("carro", data_carro[0]))
				#obtener motos del usuario
				cur.execute('SELECT * FROM moto WHERE placa = \"{}\"'.format(placa))
				data_motos = cur.fetchall()
				ingreso_motos = []
				for data_moto in data_motos:
					ingreso_motos.append(datos_parqueadero("moto", data_moto[0]))
				
				if len(data_carros) == 0 and len(data_motos) == 0:
					flash('El vehiculo no esta registrado, por favor registrelo')
					return render_template("registrar_vehiculo.html", placa_vehiculo = placa, check_carro = "checked", check_moto = "", check_bicicleta = "")

				if len(data_carros) > 0:
					return render_template("entrada_parqueadero.html", placa_carros = [data_carros, ingreso_carros])
				elif len(data_motos) > 0:
					return render_template("entrada_parqueadero.html", placa_motos = [data_motos, ingreso_motos])
	except:
		traceback.print_exc()
		flash('Error inesperado, sentimos las molestias')
		return redirect(url_for('defaul'))

@app.route('/entrada_parqueadero')
def entrada_parqueadero():
	try:
		tipos = {"c":"carro", "m":"moto", "b":"bicicleta"}
		id_vehiculo = request.args.get('ve')
		tipo = tipos[request.args.get('ty')]
		hay_celdas = hay_celdas_libres(tipo)
		if hay_celdas:
			celda = get_celda(tipo)
			cur = mysql.connection.cursor()
			query = 'INSERT INTO entrada (id_{}, id_celda) VALUES ({}, {})'.format(tipo, id_vehiculo, celda[0])
			print(query)
			cur.execute(query)
			mysql.connection.commit()
			query = 'UPDATE celda SET estado = "ocupado" WHERE id_celda = {}'.format(celda[0])
			print(query)
			cur.execute(query)
			mysql.connection.commit()
			flash('Ingreso correcto, la celda asignada es: # {}'.format(celda[1]))
			return render_template("entrada_parqueadero.html")
		else:
			flash('Ingreso fallido')
			return render_template("entrada_parqueadero.html")
	except:
		traceback.print_exc()
		flash('Error inesperado, sentimos las molestias')
		return redirect(url_for('defaul'))

@app.route('/salida_parqueadero')
def salida_parqueadero():
	try:
		tipos = {"c":"carro", "m":"moto", "b":"bicicleta"}
		id_vehiculo = request.args.get('ve')
		tipo = tipos[request.args.get('ty')]
		celda = request.args.get('cel')
		
		cur = mysql.connection.cursor()
		query = 'UPDATE entrada SET fecha_salida = now() WHERE id_{} = {} AND ISNULL(fecha_salida)'.format(tipo, id_vehiculo)
		print(query)
		cur.execute(query)
		mysql.connection.commit()
		query = 'UPDATE celda SET estado = "libre" WHERE id_celda = {}'.format(celda)
		print(query)
		cur.execute(query)
		mysql.connection.commit()
		flash('Se libero correctamente la celda')
		return render_template("entrada_parqueadero.html")
	except:
		traceback.print_exc()
		flash('Error inesperado, sentimos las molestias')
		return redirect(url_for('defaul'))

def hay_celdas_libres(tipo):
	try:
		cur = mysql.connection.cursor()
		cur.execute('SELECT * FROM celda WHERE tipo = \"{}\" and estado = \"libre\"'.format(tipo))
		celdas = cur.fetchall()
		return len(celdas)>0
	except:
		traceback.print_exc()
		return False

def get_celda(tipo):
	try:
		cur = mysql.connection.cursor()
		cur.execute('SELECT * FROM celda WHERE tipo = \"{}\" and estado = \"libre\" limit 1'.format(tipo))
		celdas = list(cur.fetchall())[0]
		return celdas
	except:
		traceback.print_exc()
		return []

def datos_parqueadero(tipo, id):
	try:
		cur = mysql.connection.cursor()
		cur.execute('SELECT consecutivo, fecha_entrada, IFNULL(fecha_salida, ""), id_carro, id_moto, id_bicicleta, id_celda FROM entrada WHERE id_{} = {} order by fecha_entrada desc'.format(tipo, id))
		celdas = cur.fetchall()
		if len(celdas)>0:
			return list(celdas)
		else:
			return []
	except:
		traceback.print_exc()
		return []

if __name__ == '__main__':
	app.run(host=acp.server_host ,port = 3000, debug = True)