from flask import Flask, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Olá mundo!</h1>"

@app.route("/greet/<usuario>/<int:idade>/")
def greet(usuario, idade):
    return f"<h1>Olá {usuario} de {idade} anos</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
