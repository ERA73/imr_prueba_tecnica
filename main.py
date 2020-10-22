from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'parqueadero'
mysql = MySQL(app)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/enrutar', methods = ['POST'])
def enrutar():
	if request.method == 'POST':
		print(request.form)
		if "crear_usuario" in request.form.keys():
			return render_template("crear_usuario.html")
		elif "registrar_vehiculo" in request.form.keys():
			return render_template("registrar_vehiculo.html")
		elif "entrada_parqueadero" in request.form.keys():
			return render_template("entrada_parqueadero.html")

@app.route('/crear_usuario', methods = ['POST'])
def crear_usuario():
	if request.method == 'POST':
		documento = request.form['documento']
		nombres = request.form['nombres']
		apellidos = request.form['apellidos']
		#print(documento)
		#print(nombres)
		#print(apellidos)
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO usuario (documento, nombres, apellidos) VALUES ({},\"{}\",\"{}\")".format(documento, nombres, apellidos))
		mysql.connection.commit()
		flash('Contacto agregado correctamente')
		return redirect(url_for('index'))

@app.route('/registrar_vehiculo', methods = ['POST'])
def registrar_vehiculo():
	if request.method == 'POST':
		print(request.form)
		return "<p>Vehiculo registrado</p>"

@app.route('/entrada_parqueadero', methods = ['POST'])
def entrada_parqueadero():
	if request.method == 'POST':
		print(request.form)
		return "<p>Entrada a parqueadero hecha</p>"

@app.route('/buscar_usuario', methods = ['POST'])
def buscar_usuario():
	if request.method == 'POST':
		print(request.form)
		return "<p>Busqueda de usuario hecha</p>"

@app.route('/buscar_vehiculo', methods = ['POST'])
def buscar_vehiculo():
	if request.method == 'POST':
		print(request.form)
		return "<p>Busqueda de vehiculo hecha</p>"

if __name__ == '__main__':
	app.run(port = 3000, debug = True)