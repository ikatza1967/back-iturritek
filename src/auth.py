from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import request, jsonify

# Cuando se llama busca el usuario
def find_user_by_username(username):
    # Ejemplos de usuarios
    users = [
        {'username': 'usuario1', 'password': 'contraseña1'},
        {'username': 'usuario2', 'password': 'contraseña2'}
    ]
    
    # Si el usuario coinicde se devuelve respuesta sino no
    for user in users:
        if user['username'] == username:
            return user
    return None

# Función para verificar la contraseña de un usuario
def verify_password(user, password):
    # Una vez la funcion anterior nos devuelve user se comprueba que la contraseña coincida
    return user['password'] == password

# Configura la extensión Flask-JWT-Extended
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def initialize_auth(app):
    app.config['JWT_SECRET_KEY'] = 'tu_clave_secreta'
    jwt.init_app(app)

@jwt_required
def protected_route():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user)
