from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import traceback

app = Flask(__name__)

# MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'parqueadero'
mysql = MySQL(app)

#settings
app.secret_key = "mysecretkey"

@app.route('/index')
def index():
	try:
		return render_template("index.html")
	except:
		traceback.print_exc()
		return "<p>Error inesperado, sentimos las molestias</p>"

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
	except:
		traceback.print_exc()
		return "<p>Error inesperado, sentimos las molestias</p>"

@app.route('/crear_usuario_form')
def crear_usuario_form():
	try:
		cur = mysql.connection.cursor()
		cur.execute('SELECT * FROM usuario')
		data = cur.fetchall()
		return render_template("crear_usuario.html", usuarios = data)
	except:
		traceback.print_exc()
		return "<p>Error inesperado, sentimos las molestias</p>"

@app.route('/registrar_vehiculo_form')
def registrar_vehiculo_form():
	try:
		return render_template("registrar_vehiculo.html")
	except:
		traceback.print_exc()
		return "<p>Error inesperado, sentimos las molestias</p>"

@app.route('/entrada_parqueadero_form')
def entrada_parqueadero_form():
	try:
		return render_template("entrada_parqueadero.html")
	except:
		traceback.print_exc()
		return "<p>Error inesperado, sentimos las molestias</p>"

@app.route('/crear_usuario', methods = ['POST'])
def crear_usuario():
	try:
		if request.method == 'POST':
			documento = request.form['documento']
			nombres = request.form['nombres']
			apellidos = request.form['apellidos']
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO usuario (documento, nombres, apellidos) VALUES ({},\"{}\",\"{}\")".format(documento, nombres, apellidos))
			mysql.connection.commit()
			flash('Contacto agregado correctamente')
			return redirect(url_for('crear_usuario_form'))
	except:
		traceback.print_exc()
		return "<p>Error inesperado, sentimos las molestias</p>"

@app.route('/registrar_vehiculo', methods = ['POST'])
def registrar_vehiculo():
	try:
		if request.method == 'POST':
			placa_carro = request.form['placa_carro']
			modelo = request.form['modelo']
			puertas = request.form['puertas']
			
			placa_moto = request.form['placa_moto']
			cilindraje = request.form['cilindraje']
			tiempos = request.form['tiempos']

			foto = ""#request.form['foto']
			documento = request.form['documento']
			print(documento)
			print(placa_carro)
			print(modelo)
			cur = mysql.connection.cursor()
			if placa_carro != "":
				cur.execute("INSERT INTO carro (placa, modelo, puertas, foto, us_documento) VALUES (\"{}\",\"{}\",{},\"{}\",{})".format(placa_carro, modelo, puertas, foto, documento))
				mysql.connection.commit()
				flash('Carro agregado correctamente')
			elif placa_moto != "":
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
		return "<p>Error inesperado, sentimos las molestias</p>"

@app.route('/buscar_usuario', methods = ['POST'])
def buscar_usuario():
	try:
		if request.method == 'POST':
			cur = mysql.connection.cursor()
			if "buscar_usuario" in request.form.keys():
				documento = request.form['documento']
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

				return render_template("entrada_parqueadero.html", usuario_carros = [data_carros, ingreso_carros], usuario_motos = [data_motos, ingreso_motos], usuario_bicicletas = [data_bicicletas, ingreso_bicicletas])
	except:
		traceback.print_exc()
		return "<p>Error inesperado, sentimos las molestias</p>"

@app.route('/buscar_vehiculo', methods = ['POST'])
def buscar_vehiculo():
	try:
		if request.method == 'POST':
			cur = mysql.connection.cursor()
			if "buscar_vehiculo" in request.form.keys():
				placa = request.form['placa']
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

				if len(data_carros) > 0:
					return render_template("entrada_parqueadero.html", placa_carros = [data_carros, ingreso_carros])
				elif len(data_motos) > 0:
					return render_template("entrada_parqueadero.html", placa_motos = [data_motos, ingreso_motos])
	except:
		traceback.print_exc()
		return "<p>Error inesperado, sentimos las molestias</p>"

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
		return "<p>Error inesperado, sentimos las molestias</p>"

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
		return "<p>Error inesperado, sentimos las molestias</p>"

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
		celdas = list(cur.fetchall())[0]
		if len(celdas)>0:
			return celdas
		else:
			return []
	except:
		traceback.print_exc()
		return []

if __name__ == '__main__':
	app.run(port = 3000, debug = True)