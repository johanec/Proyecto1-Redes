import random
import time
from datetime import datetime
import threading

# Tamaño máximo del paquete en bytes
MAX_PKT = 1024
info_hilos = {'info1': '', 'info2': ''}     #Aqui guardo todo lo que el socket va a imprimir en el html
stop = True

# Canal de comunicación, aquí guardamos los frames enviados para simular su transmisión
channel = []

# Tipos de frames
class FrameKind:
    DATA = "DATA"
    ACK = "ACK"
    NAK = "NAK"

# Representa un paquete de la capa de red
class Packet:
    def __init__(self, data=None):
        if data is None:
            self.data = bytearray(MAX_PKT)
        else:
            self.data = data

# Representa un frame de la capa de enlace
class Frame:
    def __init__(self):
        self.kind = None  # Tipo de frame
        self.seq = None   # Número de secuencia
        self.ack = None   # Número de confirmación
        self.info = Packet()  # Paquete de la capa de red

# Tipo de eventos posibles
class EventType:
    FRAME_ARRIVAL = 0
    CKSUM_ERR = 1
    TIMEOUT = 2
    ACK_TIMEOUT = 3
    NETWORK_LAYER_READY = 4

# Esperar un evento (en este caso, sólo la llegada de un frame)
def wait_for_event():
    if channel:
        return EventType.FRAME_ARRIVAL
    return None

def wait_for_event_par(tiempo_inicial):
    if int(round((datetime.now() - tiempo_inicial ).total_seconds())) < 10:
        if channel:
            num = random.randint(1, 10)
            if num == 9:
                return EventType.NETWORK_LAYER_READY
            if num > 8:
                return EventType.CKSUM_ERR
            else:
                return EventType.FRAME_ARRIVAL
        else: 
            return None
    else:
        return EventType.TIMEOUT

        
# Simula la obtención de un paquete desde la capa de red
def from_network_layer():
    data = bytearray(random.getrandbits(8) for _ in range(10))
    return Packet(data)

# Simula el envío de un frame a la capa física
def to_physical_layer(frame, socketio, machine):
    global channel
    channel.append(frame)
    
    # Determinar qué máquina está llamando a la función
    if machine == "A": # Si es la máquina A
        info_hilos['info1'] = (f"Sent frame -> Type: {frame.kind}, Sequence: {frame.seq}, Confirmation: {frame.ack}, Data: {frame.info.data}")
        info_hilos['info2'] = ("-")
        socketio.emit('actualizar_info1', info_hilos)  
        socketio.emit('actualizar_info2', info_hilos)  

    elif machine == "B": # Si es la máquina B
        info_hilos['info2'] = (f"Sent frame -> Type: {frame.kind}, Sequence: {frame.seq}, Confirmation: {frame.ack}, Data: {frame.info.data}")
        info_hilos['info1'] = ("-")
        socketio.emit('actualizar_info2', info_hilos)  
        socketio.emit('actualizar_info1', info_hilos)  

# Simula la recepción de un frame desde la capa física
def from_physical_layer(socketio, machine):
    global channel
    frame = channel.pop(0)
    
    # Determinar qué máquina está llamando a la función
    if machine == "A": # Si es la máquina A
        info_hilos['info1'] = (f"Received frame -> Type: {frame.kind}, Sequence: {frame.seq}, Confirmation: {frame.ack}, Data: {frame.info.data}")
        info_hilos['info2'] = ("-")
        socketio.emit('actualizar_info1', info_hilos)  
        socketio.emit('actualizar_info2', info_hilos)  

    elif machine == "B": # Si es la máquina B
        info_hilos['info2'] = (f"Received frame -> Type: {frame.kind}, Sequence: {frame.seq}, Confirmation: {frame.ack}, Data: {frame.info.data}")
        info_hilos['info1'] = ("-")
        socketio.emit('actualizar_info2', info_hilos)  
        socketio.emit('actualizar_info1', info_hilos)  

    return frame


# Simula el envío de un paquete a la capa de red
def to_network_layer(packet, socketio, machine):
    
    # Determinar qué máquina está llamando a la función
    if machine == "A": # Si es la máquina A
        info_hilos['info1'] = (f"Packet received at Network Layer: {packet.data}")
        info_hilos['info2'] = ("-")
        socketio.emit('actualizar_info1', info_hilos)  
        socketio.emit('actualizar_info2', info_hilos)  

    elif machine == "B": # Si es la máquina B
        info_hilos['info2'] = (f"Packet received at Network Layer: {packet.data}")
        info_hilos['info1'] = ("-")
        socketio.emit('actualizar_info2', info_hilos)  
        socketio.emit('actualizar_info1', info_hilos)  

# Funciones placeholder para timers 
def start_timer():
    return datetime.now()

def stop_timer(tiempo_inicial):
    tiempo_inicial = 0
    return tiempo_inicial

def start_ack_timer():
    pass

def stop_ack_timer():
    pass

# Funciones para habilitación/deshabilitación de capas
def enable_network_layer():
    pass

def disable_network_layer():
    pass

# Función para incrementar números de secuencia (similar a una macro en C)
def inc(k, MAX_SEQ):
    return k + 1 if k < MAX_SEQ else 0

