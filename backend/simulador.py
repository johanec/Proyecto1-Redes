import threading  # Importamos el módulo de hilos
from flask_socketio import SocketIO
import time
import utopia
import stop_and_wait
import par
import sliding
#import ...

# Agregar a la lista los nuevos protocolos
protocolos = [utopia,stop_and_wait,par,sliding]     #Contiene los protocolos(Archivos py)
activo = True         #Variable para pausar los hilos
protocolo = None      #Variable que contiene el numero del protocolo q se usará
RUNNING = True
global error
global secuencia
# Función crea un emisor dependiendo del protocolo seleccionado

def emisor(socketio):
    while RUNNING:
        if activo:
            protocolos[protocolo].sender(socketio,error,secuencia)     #LLama a la función Sender del archivo de la lista
        time.sleep(1)
    print("emisor cerrado")
    return 0

# Función crea un receptor dependiendo del protocolo seleccionado
def receptor(socketio):
    while RUNNING:
        if activo:
            protocolos[protocolo].receiver(socketio,error,secuencia)    #LLama a la función Receiver del archivo de la lista
        time.sleep(1)
    print("receptor cerrado")
    return 0

# Función crea un receptor dependiendo del protocolo seleccionado
def protocol_machineA(socketio):
    while RUNNING:
        if activo:
            protocolos[protocolo].protocol_machineA(socketio,error,secuencia)    #LLama a la función Receiver del archivo de la lista
        time.sleep(1)
    print("Maquina A cerrada")
    return 0

# Función crea un receptor dependiendo del protocolo seleccionado
def protocol_machineB(socketio):
    while RUNNING:
        if activo:
            protocolos[protocolo].protocol_machineB(socketio,error,secuencia)    #LLama a la función Receiver del archivo de la lista
        time.sleep(1)
    print("Maquina B cerrada")
    return 0

# Función que detiene la simulación 
def detener_simulacion():
    global activo
    activo = False
    sliding.pausa = True
# Función que reanuda la simulación 
def reanudar_simulacion():
    global activo
    activo = True
    sliding.pausa = False

# Función que reinicia la simulación 
def reiniciar_simulacion():
    global activo
    global RUNNING
    RUNNING = False
    activo = True

# Función que genera los hilos
def simular(socketio,num_protocolo,num_error,num_secuencia):
    global protocolo
    global RUNNING
    global error
    global secuencia
    error = num_error
    secuencia = num_secuencia
    protocolo = int(num_protocolo)
    time.sleep(2)
    RUNNING = True
    if(protocolo < 3):
        emisor_thread = threading.Thread(target=emisor,args=(socketio,))  # Creamos un hilo para el emisor
        receptor_thread = threading.Thread(target=receptor,args=(socketio,))  # Creamos un hilo para el emisor
        emisor_thread.start()  # Iniciamos el hilo del emisor
        receptor_thread.start()  # Iniciamos el hilo del emisor
    else:
        maquina_a_thread = threading.Thread(target=protocol_machineA,args=(socketio,))  # Creamos un hilo para el emisor
        maquina_b_thread = threading.Thread(target=protocol_machineB,args=(socketio,))  # Creamos un hilo para el emisor
        maquina_a_thread.start()  # Iniciamos el hilo del emisor
        maquina_b_thread.start()  # Iniciamos el hilo del emisor


