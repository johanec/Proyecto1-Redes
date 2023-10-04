# Importamos las clases y funciones del archivo protocolo.py
from protocolo import *

# Función del emisor
def sender(socketio):
    buffer = from_network_layer()  # Obtener algo para enviar desde la capa de red
    s = Frame()  # Crear un objeto frame
    s.info = buffer  # Copiamos el paquete en s para transmisión
    s.kind = FrameKind.DATA  # Set the frame kind as data
    to_physical_layer(s,socketio,"A")  # Enviamos el frame a la capa física/

# Función del receptor
def receiver(socketio):
    event = wait_for_event()  # Esperamos un evento, la única posibilidad es la llegada de un frame
    if event == EventType.FRAME_ARRIVAL:  # Si ha llegado un frame
        r = from_physical_layer(socketio,"B")  # Obtenemos el frame de la capa física
        to_network_layer(r.info,socketio,"B")  # Enviamos la información del frame a la capa de red

