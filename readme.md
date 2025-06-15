NECESARIO:
Python
PostgreSQL y PG Admin.

Video para instalar PostgreSQL con PG Admin:
IMPORTANTE: Al instalar el PostgreSQL con el PG Admin, les va a pedir que creen un usuario y contraseña
Usuario: por defecto debería ser "postgre"
Contraseña: 12345
Nombre de la BD: MaestranzasDB
https://www.youtube.com/watch?v=4qH-7w5LZsA
VER CARPETA /SQL PARA ESPECIFICACIONES DE LA BD, SUS TABLAS Y DATOS DE PRUEBA

-Para crear el ambiente virtual:
python -m venv maestranzas-env

EN WINDOWS, ABRE POWER SHELL COMO ADMINISTRADOR Y EJECUTA EL SIGUIENTE COMANDO:
Set-ExecutionPolicy RemoteSigned
Esto debes hacerlo una vez por PC para poder activar el ambiente virtual

-Para usar el ambiente virtual: 
.\maestranzas-env\Scripts\Activate
-Instalar dependencias:
pip install -r requirements.txt
-Correr el proyecto:
python .\main.py