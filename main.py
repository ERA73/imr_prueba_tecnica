from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

@app.route('/')
def index():
	return "Hola mundo"

if __name__ == '__main__':
	app.run(port = 3000, debug = True)