import sqlite3

DATABASE_URI = 'bbdd.sqlite'

try:
    db=sqlite3.connect("bbdd.sqlite")
    print("conexion exitosa")

except sqlite3.Error:
    print("error al conectar a la base de datos")


