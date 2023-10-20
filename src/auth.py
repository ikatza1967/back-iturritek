from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import request, jsonify

# Función para buscar un usuario en una estructura de datos ficticia (simulando una base de datos)
def find_user_by_username(username):
    # Simulación: supongamos que tenemos una lista de usuarios con nombres de usuario y contraseñas
    users = [
        {'username': 'usuario1', 'password': 'contraseña1'},
        {'username': 'usuario2', 'password': 'contraseña2'},
        # ... otros usuarios
    ]

    for user in users:
        if user['username'] == username:
            return user
    return None

# Función para verificar la contraseña de un usuario
def verify_password(user, password):
    # Simulación: comparamos la contraseña proporcionada con la contraseña del usuario
    return user['password'] == password

# Configura la extensión Flask-JWT-Extended
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def initialize_auth(app):
    app.config['JWT_SECRET_KEY'] = 'tu_clave_secreta'
    jwt.init_app(app)

def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = find_user_by_username(username)
    if not user or not verify_password(user, password):
        return jsonify({'message': 'Credenciales inválidas'}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@jwt_required
def protected_route():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user)
