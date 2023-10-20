#Se importa la configuracion de la bbdd
from dbConfig import get_db

#Se importamos los archivos
from src.correo import *
from src.auth import *

from flask import Flask, jsonify, g, request, render_template
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
initialize_auth(app)


# Para evitar problemas con la base de datos
@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Extensiones permitidas para el file de la img
ALLOWED_EXTENSIONS = {'png',}  
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def bienvenidos():
    return "Hola"

# Ruta para visualizar la tabla de solicitudes
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

# Ruta para visualizar los servicios
@app.route("/ver_servicios")
def get_servicios():
    cursor = get_db().cursor()
    cursor.execute('''
        SELECT 
            s.id_Servicio, 
            s.nombre_Servicio, 
            s.descripcion_Servicio, 
            s.categoria_Id, 
            c.nombre_Categoria AS nombre_categoria,
            s.img_Servicio
        FROM servicios AS s
        INNER JOIN categorias AS c ON s.categoria_Id = c.id_Categoria
    ''')
    servicios = cursor.fetchall()
    cursor.close()

    servicios_con_imagen = []
    for servicio in servicios:
        id_Servicio, nombre_Servicio, descripcion_Servicio, categoria_Id, nombre_categoria, imagen_data = servicio
        # Convertir la imagen en formato base64
        imagen_base64 = base64.b64encode(imagen_data).decode('utf-8')

        # Crear un diccionario con la información del servicio y la imagen base64
        servicio_con_imagen = {
            "id_Servicio": id_Servicio,
            "nombre_Servicio": nombre_Servicio,
            "descripcion_Servicio": descripcion_Servicio,
            "categoria_Id": categoria_Id,
            "nombre_categoria": nombre_categoria,
            "imagen_base64": imagen_base64,
        }

        servicios_con_imagen.append(servicio_con_imagen)

    return jsonify(servicios_con_imagen)

# Ruta que devuelve solo servicios con cierto id de cagtegoria
@app.route('/servicioDeCategoria/<int:id_Categoria>')
def servicioDeCategoria(id_Categoria):
    cursor = get_db().cursor()
    cursor.execute('''
        SELECT id_Servicio, nombre_Servicio, descripcion_Servicio, img_Servicio
        FROM servicios
        WHERE categoria_Id = ?
    ''', (id_Categoria,))
    
    servicios = cursor.fetchall()
    cursor.close()
    
    servicios_con_imagen = []
    for servicio in servicios:
        id_Servicio, nombre_Servicio, descripcion_Servicio, imagen_data = servicio
        # Convertir la imagen en formato base64
        imagen_base64 = base64.b64encode(imagen_data).decode('utf-8')
        
        # Crear un diccionario con la información del servicio y la imagen base64
        servicio_con_imagen = {
            "id_Servicio": id_Servicio,
            "nombre_Servicio": nombre_Servicio,
            "descripcion_Servicio": descripcion_Servicio,
            "imagen_base64": imagen_base64,
        }
        
        servicios_con_imagen.append(servicio_con_imagen)
    
    return jsonify(servicios_con_imagen)

# Ruta que recive las solicitudes desde el formulario del front y las introduce a la bbdd
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
            print(nombre_Categoria)

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
        nombre_Servicio = request.form['nombre_Servicio']
        descripcion_Servicio = request.form['descripcion_Servicio']
        categoria_Id = request.form['categoria_Id']
        img_Servicio = request.files['img_Servicio']
        
        if img_Servicio and allowed_file(img_Servicio.filename):
            imagen_data = img_Servicio.read()

            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO servicios (nombre_Servicio, descripcion_Servicio, img_Servicio, categoria_Id) VALUES (?, ?, ?, ?)", (nombre_Servicio, descripcion_Servicio, imagen_data, categoria_Id))
            db.commit()
            cursor.close()

            return "Servicio creado exitosamente"
        else:
            return "Error al cargar la imagen o el formato no está permitido"
    return "Método no permitido"

# Ruta para eliminar una categoria   
@app.route("/eliminar_categoria/<int:id_categoria>", methods=["DELETE"])
def eliminar_categoria(id_categoria):
    if request.method == "DELETE":
        try:
            db = get_db()
            cursor = db.cursor()
            
            # Verificar si la categoría existe antes de eliminarla
            cursor.execute("SELECT id_Categoria FROM categorias WHERE id_Categoria = ?", (id_categoria,))
            categoria = cursor.fetchone()
            
            if categoria is not None:
                # Eliminar la categoría por su ID
                cursor.execute("DELETE FROM categorias WHERE id_Categoria = ?", (id_categoria,))
                db.commit()
                cursor.close()
                return jsonify({"mensaje": "Categoría eliminada correctamente"})
            else:
                return jsonify({"error": "La categoría no existe"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "Método no permitido"}), 405

# Ruta para eliminar un servicio   
@app.route("/eliminar_servicio/<int:id_Servicio>", methods=["DELETE"])
def eliminar_servicio(id_Servicio):
    if request.method == "DELETE":
        try:
            db = get_db()
            cursor = db.cursor()
            
            # Verificar si la categoría existe antes de eliminarla
            cursor.execute("SELECT id_Servicio FROM servicios WHERE id_Servicio = ?", (id_Servicio,))
            servicio = cursor.fetchone()
            
            if servicio is not None:
                # Eliminar la categoría por su ID
                cursor.execute("DELETE FROM servicios WHERE id_Servicio = ?", (id_Servicio,))
                db.commit()
                cursor.close()
                return jsonify({"mensaje": "Servicio eliminado correctamente"})
            else:
                return jsonify({"error": "El servicio no existe"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "Método no permitido"}), 405
    
# Ruta para el inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = find_user_by_username(username)

    if user and verify_password(user, password):
        # Si las credenciales son válidas, crea un token JWT
        access_token = create_access_token(identity=username)
        print("Inicio de sesión exitoso. Token JWT generado.")
        return jsonify(access_token=access_token)
    else:
        print("Inicio de sesión fallido. Credenciales inválidas.")
        return jsonify({'message': 'Credenciales inválidas'}), 401

# Ruta que pide el token para acceder a la intranet
@app.route('/intranet', methods=['GET'])
@jwt_required
def intranet():
    current_user = get_jwt_identity()
    return jsonify(message=f'Bienvenido a la intranet, {current_user}!')