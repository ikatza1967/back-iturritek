from dbConfig import get_db
from flask import Flask, jsonify, g, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def bienvenidos():
    return "Hola"

@app.route("/prueba")
def get_usuarios():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    return jsonify(usuarios)

@app.route("/recibir_datos", methods=["POST"])
def recibir_datos():
    if request.method == "POST":
        # Obtener datos del formulario o del cuerpo JSON de la solicitud
        user_data = request.json  # Esto asume que los datos se envían en formato JSON

        if user_data:
            # Puedes procesar los datos y guardarlos en la base de datos
            user_name = user_data.get("user_name")
            user_surname = user_data.get("user_surname")
            user_tel = user_data.get("user_tel")
            user_email = user_data.get("user_email")
            selected_option = user_data.get("select")
            message = user_data.get("message")

            # Insertar los datos en la base de datos
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
    

if __name__ == "__main__":
    app.run(debug=True)
