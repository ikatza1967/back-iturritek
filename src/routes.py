from dbConfig import get_db
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
@app.route("/ver_usuarios")
def get_usuarios():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    return jsonify(usuarios)

# Ruta que recive los usuarios desde el formulario del front y los introduce a la bbdd
@app.route("/recibir_datos", methods=["POST"])
def recibir_datos():
    if request.method == "POST":
        user_data = request.json
        print(user_data)
        if user_data:
            user_name = user_data.get("user_name")
            user_surname = user_data.get("user_surname")
            user_tel = user_data.get("user_tel")
            user_email = user_data.get("user_email")
            selected_option = user_data.get("select")
            message = user_data.get("message")

            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO usuarios (nombre, apellidos, telefono, email, servicio, mensaje) VALUES (?, ?, ?, ?, ?, ?)",
                           (user_name, user_surname, user_tel, user_email, selected_option, message))
            db.commit()
            cursor.close()

            return "Datos guardados exitosamente en la base de datos"
        else:
            return jsonify({"error": "No se recibieron datos válidos"}), 400
    else:
        return jsonify({"error": "Método no permitido"}), 405
    

