Como poner en marcha la app:
- se debe tener instalado python y posteriormente la libreria Flask y flask_mysqldb
- instalar la BD usando el archivo "SQL/install_mariadb.bat", el cual insalara el motor de base de datos con los ajustes necesarios.
	NOTA: si desae puede editar el archivo y cambiar la configuracion pero recuerde que la informacion debe coincidir con la seccion de configuracion "MySQL connection" del archivo "main.py"
- ejecutar el archivo "SQL/load_db.bat" pra cargar la base de datos y poblarla con algunos datos
- par poner en marcha la app, ejecutar el archivo "main.py"
- para usar la app web, ingese a la direccion "localhost:3000" o "127.0.0.1:3000"


A continuacion se describen los archivos y directorios que componen la app:
- Directorio SQL:
	En este directorio se encuentran los archivos necesarios para el funcionamiento de la base de datos, se describen a continuacion:
	- install_mariadb.bat : Se encarga de instalar de forma desatendida el motor de BD MariaDB, el cuan configura el usuario y contraseña(root, admin), etc.
	- mariadb.msi : Archivo que se usa para la instalacion de MariaDB
	- load_db.bat y copy_db.bat : Hacen carga o respaldo de la base de datos.
	- Parqueadero_ER.png : Diagrama ER
	- db_backup_company.sql : Archivo que contiene las instrucciones de creacion de la BD y datos para poblarla
- Directorio templates:
	- contiene los archivos HTML de las vistas
- Directorio stacic/images:
	- contiene la imagen de IMR que usa la vista
- Directorio static/script:
	- contiene la controladora con código javascript
- Archivo dao.py:
	- contiene una clase que se encarga de construir las consultas SQL
- Archivo main.py:
	- es el archivo principal, el cual pone en marcha la app