import sqlite3
from flask import g

DATABASE_URI = 'bbdd.sqlite'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        try:
            db = g._database = sqlite3.connect(DATABASE_URI)
            print("Conexión exitosa a la base de datos")
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
    return db
