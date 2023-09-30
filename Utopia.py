# Importamos las clases y funciones del archivo Protocolo.py
from Protocolo import Frame, FrameKind, Packet, from_network_layer, to_physical_layer, wait_for_event, from_physical_layer, EventType, to_network_layer
import threading  # Importamos el módulo de hilos
import time  # Importamos el módulo de tiempo para pausas

RUNNING = True  # Una variable para controlar la ejecución

# Función del emisor
def sender1():
    while RUNNING:  # Mientras esté en ejecución
        buffer = from_network_layer()  # Obtener algo para enviar desde la capa de red
        s = Frame()  # Crear un objeto frame
        s.info = buffer  # Copiamos el paquete en s para transmisión
        s.kind = FrameKind.DATA  # Set the frame kind as data
        to_physical_layer(s)  # Enviamos el frame a la capa física

# Función del receptor
def receiver1():
    while RUNNING:  # Mientras esté en ejecución
        event = wait_for_event()  # Esperamos un evento, la única posibilidad es la llegada de un frame
        if event == EventType.FRAME_ARRIVAL:  # Si ha llegado un frame
            r = from_physical_layer()  # Obtenemos el frame de la capa física
            to_network_layer(r.info)  # Enviamos la información del frame a la capa de red

# Función principal del Protocolo Utopia
def Utopia_protocol():
    global RUNNING  # Declaramos la variable global para modificarla posteriormente
    sender_thread = threading.Thread(target=sender1)  # Creamos un hilo para el emisor
    receiver_thread = threading.Thread(target=receiver1)  # Creamos un hilo para el receptor
    sender_thread.start()  # Iniciamos el hilo del emisor
    receiver_thread.start()  # Iniciamos el hilo del receptor
    time.sleep(5)  # Dejamos que se ejecute durante 5 segundos
    RUNNING = False  # Esto detendrá los bucles dentro de sender1 y receiver1
    sender_thread.join()  # Esperamos a que termine el hilo del emisor
    receiver_thread.join()  # Esperamos a que termine el hilo del receptor

# Punto de entrada principal
if __name__ == "__main__":
    print("Starting the Utopia Protocol Simulation...")
    Utopia_protocol()  # Llamamos a la función principal
    print("¡Simulation finished!")
