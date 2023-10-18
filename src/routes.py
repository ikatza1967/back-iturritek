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
def get_solicitudes():
    cursor = get_db().cursor()
    cursor.execute('''
        SELECT solicitudes.id, 
            solicitudes.nombre, 
            solicitudes.apellidos, 
            solicitudes.telefono, 
            solicitudes.email, 
            servicios.nombre_servicio AS servicio, 
            categorias.nombre_Categoria AS categoria, 
            solicitudes.mensaje
        FROM solicitudes
        INNER JOIN servicios ON solicitudes.servicio_Id = servicios.id_Servicio
        INNER JOIN categorias ON servicios.categoria_Id = categorias.id_Categoria;
    ''')
    solicitudes = cursor.fetchall()
    cursor.close()
    return jsonify(solicitudes)

# Ruta para visualizar las categorias
@app.route("/ver_categorias")
def get_categorias():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()
    cursor.close()
    return jsonify(categorias)

# Ruta para visualizar las categorias
@app.route("/ver_servicios")
def get_servicios():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM servicios")
    servicios = cursor.fetchall()
    cursor.close()
    return jsonify(servicios)

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
            cursor.execute("INSERT INTO solicitudes (nombre, apellidos, telefono, email, servicio_Id, mensaje) VALUES (?, ?, ?, ?, ?, ?)",
                           (user_name, user_surname, user_tel, user_email, selected_option, message))
            db.commit()
            cursor.close()

            if enviar_correo(user_name, user_surname, user_tel, user_email, selected_option, message):
                ## En caso de que no haya ningun error
                if enviar_correo_cliente(user_name, user_email):
                    return "Todo correcto"
                return "Datos guardados en la base y correo enviado, pero correo al cliente fallido"
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
        
# Ruta Para agregar Servicios
@app.route("/agregar_servicio", methods=['POST'])
def agregar_servicio():
    if request.method == 'POST':
        servicio_data = request.json
        if servicio_data:
            nombre_Servicio = servicio_data.get('nombre_Servicio')
            descripcion_Servicio = servicio_data.get('descripcion_Servicio')
            img_Servicio = servicio_data.get('img_Servicio')
            categoria_Id = servicio_data.get('categoria_Id')

            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO servicios (nombre_Servicio, descripcion_Servicio, img_Servicio, categoria_Id) VALUES (?, ?, ?, ?)", (nombre_Servicio, descripcion_Servicio, img_Servicio, categoria_Id))
            db.commit()
            cursor.close()

            return "servicio creado exitosamente"
        else:
            return "error al crear el servicio"