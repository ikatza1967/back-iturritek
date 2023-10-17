import sqlite3
from flask import g

# En este archivo se conecta la bbdd 

DATABASE_URI = 'bbdd.sqlite'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        try:
            db = g._database = sqlite3.connect(DATABASE_URI)
            cursor = db.cursor()

            # Crea la tabla si no existe
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS solicitudes (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT,
                    apellidos TEXT,
                    telefono TEXT,
                    email TEXT,
                    servicio TEXT,
                    mensaje TEXT
                )
            ''')
            db.commit()
            
            print("Conexión exitosa a la base de datos")
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
    return db
