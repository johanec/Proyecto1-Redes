# Importamos las clases y funciones del archivo protocolo.py
from protocolo import *
import time  # Importamos el módulo de tiempo para pausas
from datetime import datetime

RUNNING = True  # Una variable para controlar la ejecución
turnoS = True
turnoR = False
tiempo_inicial = datetime.now()

flag = False

MAX_SEQ = 1

# Función del emisor
def sender(socketio,error,___secuencia):
    global tiempo_inicial
    next_frame_to_send = 0
    buffer = from_network_layer()  # Obtener algo para enviar desde la capa de red
    s = Frame()  # Crear un objeto frame
    global flag
    global turnoS
    global turnoR
    if flag == False: 
        s.info = buffer  # Copiamos el paquete en s para transmisión
        s.kind = FrameKind.DATA  # Set the frame kind as data
        s.seq = next_frame_to_send
        print("Sender: envia el primer paquete")
        to_physical_layer(s,socketio,"A")  # Enviamos el frame a la capa física
        tiempo_inicial = start_timer()
        time.sleep(3)
        flag = True
        turnoS = False
        turnoR = True
    else:
        if turnoS == True:
            event = wait_for_event(error,"par",tiempo_inicial) 
            
            if event == EventType.FRAME_ARRIVAL:  # Si ha llegado un frame
                print("Sender: recibe el acknowledge")
                s = from_physical_layer(socketio,"A")  # Obtenemos el frame de la capa física
                if (s.ack == next_frame_to_send):
                    buffer = from_network_layer()
                    next_frame_to_send = inc(next_frame_to_send,MAX_SEQ)
                    tiempo_inicial = datetime.now()

                s.info = buffer  # Copiamos el paquete en s para transmisión
                s.kind = FrameKind.DATA  # Set the frame kind as data
                s.seq = next_frame_to_send
                print("Sender: envia el paquete que sigue en la secuencia")
                to_physical_layer(s,socketio,"A")  # Enviamos el frame a la capa física
                tiempo_inicial = start_timer()
                turnoS = False
                turnoR = True
                
            else:
                from_physical_layer(socketio,"A") #Saca el frame invalido de la lista
                s.info = buffer  # Copiamos el paquete en s para transmisión
                s.kind = FrameKind.DATA  # Set the frame kind as data
                s.seq = next_frame_to_send
                print("Sender: vuelve a enviar el paquete dañado")
                to_physical_layer(s,socketio,"A")  # Enviamos el frame a la capa física
                tiempo_inicial = start_timer()
                turnoS = False
                turnoR = True

# Función del receptor
def receiver(socketio,error,___secuencia):
    frame_espected = 0
    r = Frame()
    s = Frame()
    global turnoR
    global turnoS
    if turnoR:
        event = wait_for_event(error,"par",tiempo_inicial)  
        if event == EventType.FRAME_ARRIVAL:  # Si ha llegado un frame
            print("Reciver: recive un paquete")
            r = from_physical_layer(socketio,"B")  # Obtenemos el frame de la capa física
            if (r.seq == frame_espected):
                to_network_layer(r.info,socketio,"B")  # Enviamos la información del frame a la capa de red
                frame_espected = inc(frame_espected,MAX_SEQ)
            s.info = Packet("Acknowledge!")  # Se envia un dummy para confirmarle al emisor
            s.ack = 1 - frame_espected
            print("Reciver se envia el acknowledge")
            to_physical_layer(s,socketio,"B")
            turnoS = True
            turnoR = False
