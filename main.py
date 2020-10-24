from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

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
	return render_template("index.html")

@app.route('/enrutar', methods = ['POST'])
def enrutar():
	if request.method == 'POST':
		print(request.form)
		if "crear_usuario" in request.form.keys():
			return redirect(url_for('crear_usuario_form'))
		elif "registrar_vehiculo" in request.form.keys():
			return redirect(url_for('registrar_vehiculo_form'))
		elif "entrada_parqueadero" in request.form.keys():
			return redirect(url_for('entrada_parqueadero_form'))

@app.route('/crear_usuario_form')
def crear_usuario_form():
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM usuario')
	data = cur.fetchall()
	return render_template("crear_usuario.html", usuarios = data)

@app.route('/registrar_vehiculo_form')
def registrar_vehiculo_form():
	return render_template("registrar_vehiculo.html")

@app.route('/entrada_parqueadero_form')
def entrada_parqueadero_form():
	return render_template("entrada_parqueadero.html")

@app.route('/crear_usuario', methods = ['POST'])
def crear_usuario():
	if request.method == 'POST':
		documento = request.form['documento']
		nombres = request.form['nombres']
		apellidos = request.form['apellidos']
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO usuario (documento, nombres, apellidos) VALUES ({},\"{}\",\"{}\")".format(documento, nombres, apellidos))
		mysql.connection.commit()
		flash('Contacto agregado correctamente')
		return redirect(url_for('crear_usuario_form'))

@app.route('/registrar_vehiculo', methods = ['POST'])
def registrar_vehiculo():
	if request.method == 'POST':
		placa_carro = request.form['placa_carro']
		modelo = request.form['modelo']
		puertas = request.form['puertas']
		foto = ""#request.form['foto']
		documento = request.form['documento']
		print(documento)
		print(placa_carro)
		print(modelo)
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO carro (placa, modelo, puertas, foto, us_documento) VALUES (\"{}\",\"{}\",{},\"{}\",{})".format(placa_carro, modelo, puertas, foto, documento))
		mysql.connection.commit()
		flash('Carro agregado correctamente')
		return redirect(url_for('crear_usuario_form'))

@app.route('/entrada_parqueadero', methods = ['POST'])
def entrada_parqueadero():
	if request.method == 'POST':
		print(request.form)
		return "<p>Entrada a parqueadero hecha</p>"

@app.route('/buscar_usuario', methods = ['POST'])
def buscar_usuario():

	if request.method == 'POST':
		cur = mysql.connection.cursor()
		if "buscar_usuario" in request.form.keys():
			documento = request.form['documento']
			#obtener carros del usuario
			cur.execute('SELECT * FROM carro WHERE us_documento = {}'.format(documento))
			data_carros = cur.fetchall()
			#obtener motos del usuario
			cur.execute('SELECT * FROM moto WHERE us_documento = {}'.format(documento))
			data_motos = cur.fetchall()
			#obtener bicicletas del usuario
			cur.execute('SELECT * FROM bicicleta WHERE us_documento = {}'.format(documento))
			data_bicicletas = cur.fetchall()

			return render_template("entrada_parqueadero.html", usuario_carros = data_carros, usuario_motos = data_motos, usuario_bicicletas = data_bicicletas)

@app.route('/buscar_vehiculo', methods = ['POST'])
def buscar_vehiculo():
	if request.method == 'POST':
		cur = mysql.connection.cursor()
		if "buscar_vehiculo" in request.form.keys():
			placa = request.form['placa']
			#obtener carros del usuario
			cur.execute('SELECT * FROM carro WHERE placa = \"{}\"'.format(placa))
			data_carros = cur.fetchall()
			#obtener motos del usuario
			cur.execute('SELECT * FROM moto WHERE placa = \"{}\"'.format(placa))
			data_motos = cur.fetchall()
			if len(data_carros) > 0:
				return render_template("entrada_parqueadero.html", placa_carros = data_carros)
			elif len(data_motos) > 0:
				return render_template("entrada_parqueadero.html", placa_motos = data_motos)

if __name__ == '__main__':
	app.run(port = 3000, debug = True)