import threading  # Importamos el módulo de hilos
from flask_socketio import SocketIO
import time
import utopia
import stop_and_wait
import par
#import ...

# Agregar a la lista los nuevos protocolos
protocolos = [utopia,stop_and_wait,par]     #Contiene los protocolos(Archivos py)
activo = True         #Variable para pausar los hilos
protocolo = None      #Variable que contiene el numero del protocolo q se usará
RUNNING = True
# Función crea un emisor dependiendo del protocolo seleccionado
def emisor(socketio):
    while RUNNING:
        if activo:
            protocolos[protocolo].sender(socketio)     #LLama a la función Sender del archivo de la lista
        time.sleep(1)
    print("emisor cerrado")
    return 0
# Función crea un receptor dependiendo del protocolo seleccionado
def receptor(socketio):
    while RUNNING:
        if activo:
            protocolos[protocolo].receiver(socketio)    #LLama a la función Receiver del archivo de la lista
        time.sleep(1)
    print("receptor cerrado")
    return 0

# Función que detiene la simulación 
def detener_simulacion():
    global activo
    activo = False
# Función que reanuda la simulación 
def reanudar_simulacion():
    global activo
    activo = True

# Función que reinicia la simulación 
def reiniciar_simulacion():
    global activo
    global RUNNING
    RUNNING = False
    activo = True

# Función que genera los hilos
def simular(socketio,num_protocolo):
    global protocolo
    global RUNNING
    protocolo = int(num_protocolo)
    time.sleep(2)
    RUNNING = True
    emisor_thread = threading.Thread(target=emisor,args=(socketio,))  # Creamos un hilo para el emisor
    receptor_thread = threading.Thread(target=receptor,args=(socketio,))  # Creamos un hilo para el emisor
    emisor_thread.start()  # Iniciamos el hilo del emisor
    receptor_thread.start()  # Iniciamos el hilo del emisor
