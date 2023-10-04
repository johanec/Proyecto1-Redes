# Importamos las clases y funciones del archivo Protocolo.py
import threading
from protocolo import *
import time  # Importamos el módulo de tiempo para pausas
from datetime import datetime

RUNNING = True  # Una variable para controlar la ejecución
tiempo_inicial = datetime.now()
MAX_SEQ = 1

turnoA = True
turnoB = False

# Función del emisor
def protocol_machineA(socketio,error,___secuencia):
    print("turno A")
    global turnoA
    global turnoB

    global tiempo_inicial
    next_frame_to_send = 0  # Inicializa el próximo frame a enviar
    frame_expected = 0  # Inicializa el frame que espera recibir
    buffer = from_network_layer()  # Obtiene un paquete desde la capa de red para enviar

    s = Frame()  # Crea un nuevo frame
    s.info = buffer  # Inserta el paquete en el frame
    s.seq = next_frame_to_send  # Establece el número de secuencia del frame
    s.ack = 1 - frame_expected  # Establece el número de acuse de recibo, que es el inverso del frame esperado

    
    to_physical_layer(s,socketio,"A")  # Enviamos el frame a la capa física
    tiempo_inicial = start_timer()

    turnoA = False
    turnoB = True

    # Bucle infinito para continuar enviando y recibiendo frames
    while True:
        if turnoA:
            print("turno A")
            event = wait_for_event(error,"sliding",tiempo_inicial)  # Espera un evento, que puede ser la llegada de un frame, un error de suma de comprobación o un tiempo agotado
            
            # Si se recibe un frame
            if event == EventType.FRAME_ARRIVAL:
                r = from_physical_layer(socketio,"A")  # Obtiene el frame de la capa física
                
                if r is None:  # Si no se recibió ningún frame, continua con la siguiente iteración del bucle
                    continue

                # Si el número de secuencia del frame recibido es el esperado
                if r.seq == frame_expected:
                    to_network_layer(r.info,socketio,"A")  # Envía el paquete del frame a la capa de red
                    frame_expected = 1 - frame_expected  # Invierte el número de secuencia esperado
                
                # Si el número de acuse de recibo es el esperado
                if r.ack == next_frame_to_send:
                    buffer = from_network_layer()  # Obtiene un nuevo paquete desde la capa de red para enviar
                    next_frame_to_send = 1 - next_frame_to_send  # Invierte el número de secuencia a enviar
            
            # Si ocurre un error de suma de comprobación
            elif event == EventType.CKSUM_ERR:
                print("Checksum Error!")
                # Aquí se podría manejar la retransmisión si fuera necesario

            # Prepara el próximo frame a enviar
            s.info = buffer
            s.seq = next_frame_to_send
            s.ack = 1 - frame_expected
            
            to_physical_layer(s,socketio,"A")  # Envía el frame a la capa física
            tiempo_inicial = start_timer()

            turnoA = False
            turnoB = True

def protocol_machineB(socketio,error,___secuencia):

    global turnoA
    global turnoB
    global tiempo_inicial

    next_frame_to_send = 0  # Inicializa el próximo frame a enviar
    frame_expected = 0  # Inicializa el frame que espera recibir
    buffer = from_network_layer()  # Obtiene un paquete desde la capa de red para enviar

    s = Frame()  # Crea un nuevo frame
    s.info = buffer  # Inserta el paquete en el frame
    s.seq = next_frame_to_send  # Establece el número de secuencia del frame
    s.ack = 1 - frame_expected  # Establece el número de acuse de recibo, que es el inverso del frame esperado
    
    # Bucle infinito para continuar enviando y recibiendo frames
    while True:
        if turnoB:
            print("turno B")
            event = wait_for_event(error,"sliding",tiempo_inicial)  # Espera un evento, que puede ser la llegada de un frame, un error de suma de comprobación o un tiempo agotado
            
            # Si se recibe un frame
            if event == EventType.FRAME_ARRIVAL:
                r = from_physical_layer(socketio,"B")  # Obtiene el frame de la capa física
                
                if r is None:  # Si no se recibió ningún frame, continua con la siguiente iteración del bucle
                    continue

                # Si el número de secuencia del frame recibido es el esperado
                if r.seq == frame_expected:
                    to_network_layer(r.info,socketio,"B")  # Envía el paquete del frame a la capa de red
                    frame_expected = 1 - frame_expected  # Invierte el número de secuencia esperado
                
                # Si el número de acuse de recibo es el esperado
                if r.ack == next_frame_to_send:
                    buffer = from_network_layer()  # Obtiene un nuevo paquete desde la capa de red para enviar
                    next_frame_to_send = 1 - next_frame_to_send  # Invierte el número de secuencia a enviar
            
            # Si ocurre un error de suma de comprobación
            elif event == EventType.CKSUM_ERR:
                print("Checksum Error!")
                # Aquí se podría manejar la retransmisión si fuera necesario

            # Prepara el próximo frame a enviar
            s.info = buffer
            s.seq = next_frame_to_send
            s.ack = 1 - frame_expected
            
            to_physical_layer(s,socketio,"B")  # Envía el frame a la capa física
            tiempo_inicial = start_timer()
            turnoA = True
            turnoB = False
