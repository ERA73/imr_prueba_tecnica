@ECHO OFF
ECHO Instalando Base de Datos...
"msiexec" /i "mariadb.msi" PORT=3306 PASSWORD=admin SERVICENAME=MySQL ADDLOCAL=ALL REMOVE=DEVEL,HeidiSQL INSTALLDIR="C:\mariadb" /L*v log1.txt /qb
ECHO Presione cualquier tecla para terminar...
PAUSE >nul