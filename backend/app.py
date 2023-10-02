from flask import Flask, render_template, request,jsonify
from flask_socketio import SocketIO
from simulador import simular,detener_simulacion,reanudar_simulacion,reiniciar_simulacion
import os
import sys

app = Flask(__name__)               #Inicia la app
socketio = SocketIO(app)            #Prende Sockets q escucharan acciones
app.template_folder='../frontend/templates'     #Ruta del front html
app.static_folder = '../frontend/static'        #Ruta del front style

# Ruta para mostrar la página HTML
@app.route('/')
def mostrar_pagina():
    return render_template('index.html')

# Señal del socket para pausar un evento
@socketio.on('pausar')
def pausar():
    detener_simulacion()

# Señal del socket para reanudar un evento
@socketio.on('reanudar')
def reanudar():
    reanudar_simulacion()

@socketio.on('reiniciar')
def reiniciar():
    reiniciar_simulacion()

# Ruta que crea la simulación, manda el protocolo seleccionado
@app.route('/simular', methods=['POST'])
def procesar_formulario():
    if request.method == 'POST':                    #Obtiene el formulario del HTML
        protocolo = request.form.get("protocolo")   #Saca el valor del formulario con la etiqueta "protocolo"
        simular(socketio,protocolo)                 #Paso datos a "simulador.py"
        return render_template('index.html')        #Muestro de nuevo el HTML 

if __name__ == '__main__':
    socketio.run(app, debug=True)
