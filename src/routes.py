from dbConfig import *

from flask import Flask

app = Flask(__name__)

@app.route("/")
def bienvenidos():
    return "hola"

@app.route("/prueba")
def get_usuarios():
    cursor=db.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios=cursor.fetchall()
    cursor.close()
    return jsonify(usuarios)

if __name__=="__main__":
    app.run (debug=True)
    
