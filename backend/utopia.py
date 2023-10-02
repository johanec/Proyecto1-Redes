# Importamos las clases y funciones del archivo Protocolo.py
from protocolo import Frame, FrameKind, Packet, from_network_layer, to_physical_layer, wait_for_event, from_physical_layer, EventType, to_network_layer

# Función del emisor
def sender(socketio):
    buffer = from_network_layer()  # Obtener algo para enviar desde la capa de red
    s = Frame()  # Crear un objeto frame
    s.info = buffer  # Copiamos el paquete en s para transmisión
    s.kind = FrameKind.DATA  # Set the frame kind as data
    to_physical_layer(s,socketio)  # Enviamos el frame a la capa física/

# Función del receptor
def receiver(socketio):
    event = wait_for_event()  # Esperamos un evento, la única posibilidad es la llegada de un frame
    if event == EventType.FRAME_ARRIVAL:  # Si ha llegado un frame
        r = from_physical_layer(socketio)  # Obtenemos el frame de la capa física
        to_network_layer(r.info,socketio)  # Enviamos la información del frame a la capa de red
