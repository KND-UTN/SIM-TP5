from flask import Flask, render_template, request, jsonify
from simulador import Simulacion

app = Flask(__name__, template_folder='templates',
            static_url_path='',
            static_folder='static')

@app.route("/")
def hello():
    return render_template('index.html')


@app.route("/principal", methods=["GET"])
def principal():
    argumentos = request.args
    desde = int(argumentos.get('desde'))
    hasta = int(argumentos.get('hasta'))
    cant = int(argumentos.get('cant'))
    resultado = Simulacion(cant, desde, hasta).get_table()
    response = jsonify(resultado)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/pacientes", methods=["GET"])
def pacientes():
    resultado = Simulacion.get_pacientes_json()
    response = jsonify(resultado)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

app.run(host='0.0.0.0')