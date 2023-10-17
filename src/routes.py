#Se importa la configuracion de la bbdd
from dbConfig import get_db

#Se importa el archivo para el envio de correos
from src.correo import *

from flask import Flask, jsonify, g, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Para evitar problemas con la base de datos
@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def bienvenidos():
    return "Hola"

# Ruta para visualizar la tabla de usuarios
@app.route("/ver_solicitudes")
def get_categorias():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM solicitudes")
    usuarios = cursor.fetchall()
    cursor.close()
    return jsonify(usuarios)

# Ruta para visualizar las categorias
@app.route("/ver_categorias")
def get_usuarios():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM categorias")
    usuarios = cursor.fetchall()
    cursor.close()
    return jsonify(usuarios)

# Ruta que recive los usuarios desde el formulario del front y los introduce a la bbdd
@app.route("/recibir_datos", methods=["POST"])
def recibir_datos():
    if request.method == "POST":
        user_data = request.json
        if user_data:
            user_name = user_data.get("user_name")
            user_surname = user_data.get("user_surname")
            user_tel = user_data.get("user_tel")
            user_email = user_data.get("user_email")
            selected_option = user_data.get("select")
            message = user_data.get("message")

            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO solicitudes (nombre, apellidos, telefono, email, servicio, mensaje) VALUES (?, ?, ?, ?, ?, ?)",
                           (user_name, user_surname, user_tel, user_email, selected_option, message))
            db.commit()
            cursor.close()

            if enviar_correo(user_name, user_surname, user_tel, user_email, selected_option, message):
                ## En caso de que no haya ningun error
                return "Datos guardados en la base y correo enviado"
            else:
                ## En caso de que enviar_correo de errror
                return jsonify({"error":"Datos guardados en la base de datos, pero hubo un error al enviar el correo"})
        else:
            ## Demas errores posibles
            return jsonify({"error": "No se recibieron datos válidos"}), 400
    else:
        return jsonify({"error": "Método no permitido"}), 405
    
# Ruta Para agregar Categorias
@app.route("/agregar_categoria", methods=['POST'])
def agregar_categoria():
    if request.method == 'POST':
        categoria_data = request.json
        if categoria_data:
            nombre_Categoria = categoria_data.get('nombre_Categoria')

            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO categorias (nombre_Categoria) VALUES (?)", (nombre_Categoria,))
            db.commit()
            cursor.close()

            return "categoria creada exitosamente"
        else:
            return "error al crear la categoria"