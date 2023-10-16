from dbConfig import get_db
from flask import Flask, jsonify, g

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)
