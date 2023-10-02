# Importamos las clases y funciones del archivo Protocolo.py
from Protocolo import Frame, FrameKind, Packet, inc,start_timer,from_network_layer, to_physical_layer, wait_for_event, wait_for_event_par, from_physical_layer, EventType, to_network_layer
import threading  # Importamos el módulo de hilos
import time  # Importamos el módulo de tiempo para pausas
from datetime import datetime


RUNNING = True  # Una variable para controlar la ejecución
turnoS = True
turnoR = False
tiempo_inicial = datetime.now()

MAX_SEQ = 1

# Función del emisor
def sender3():
    global tiempo_inicial
    next_frame_to_send = 0
    buffer = from_network_layer()  # Obtener algo para enviar desde la capa de red
    s = Frame()  # Crear un objeto frame

    flag = False
    global turnoS
    global turnoR

    while RUNNING:  # Mientras esté en ejecución
        if flag == False: 
            s.info = buffer  # Copiamos el paquete en s para transmisión
            s.kind = FrameKind.DATA  # Set the frame kind as data
            s.seq = next_frame_to_send
            print("Sender: envia el primer paquete")
            to_physical_layer(s)  # Enviamos el frame a la capa física
            tiempo_inicial = start_timer()
            time.sleep(3)
            flag = True
            turnoS = False
            turnoR = True
        else:
            if turnoS == True:
                event = wait_for_event_par(tiempo_inicial)  # Esperamos un evento, la única posibilidad es la llegada de un frame
                
                if event == EventType.FRAME_ARRIVAL:  # Si ha llegado un frame
                    print("Sender: recibe el acknowledge")
                    s = from_physical_layer()  # Obtenemos el frame de la capa física
                    if (s.ack == next_frame_to_send):
                        buffer = from_network_layer()
                        next_frame_to_send = inc(next_frame_to_send,MAX_SEQ)
                        tiempo_inicial = datetime.now()


                    s.info = buffer  # Copiamos el paquete en s para transmisión
                    s.kind = FrameKind.DATA  # Set the frame kind as data
                    s.seq = next_frame_to_send
                    print("Sender: envia el paquete que sigue en la secuencia")
                    to_physical_layer(s)  # Enviamos el frame a la capa física
                    tiempo_inicial = start_timer()
                    turnoS = False
                    turnoR = True
                    
                else:
                    s.info = buffer  # Copiamos el paquete en s para transmisión
                    s.kind = FrameKind.DATA  # Set the frame kind as data
                    s.seq = next_frame_to_send
                    print("Sender: vuelve a enviar el paquete dañado")
                    to_physical_layer(s)  # Enviamos el frame a la capa física
                    tiempo_inicial = start_timer()
                    turnoS = False
                    turnoR = True

# Función del receptor
def receiver3():

    frame_espected = 0
    r = Frame()
    s = Frame()
    global turnoR
    global turnoS
    while RUNNING:  # Mientras esté en ejecución
        if turnoR:
            event = wait_for_event()  # Esperamos un evento, la única posibilidad es la llegada de un frame
            if event == EventType.FRAME_ARRIVAL:  # Si ha llegado un frame
                print("Reciver: recive un paquete")
                r = from_physical_layer()  # Obtenemos el frame de la capa física
                if (r.seq == frame_espected):
                    to_network_layer(r.info)  # Enviamos la información del frame a la capa de red
                    frame_espected = inc(frame_espected,MAX_SEQ)
                s.info = Packet("Acknowledge!")  # Se envia un dummy para confirmarle al emisor
                s.ack = 1 - frame_espected
                print("Reciver se envia el acknowledge")
                to_physical_layer(s)
                turnoS = True
                turnoR = False
        else:
            pass

# Función principal del Protocolo Utopia
def par_protocol():
    global RUNNING  # Declaramos la variable global para modificarla posteriormente
    sender_thread = threading.Thread(target=sender3)  # Creamos un hilo para el emisor
    receiver_thread = threading.Thread(target=receiver3)  # Creamos un hilo para el receptor
    sender_thread.start()  # Iniciamos el hilo del emisor
    receiver_thread.start()  # Iniciamos el hilo del receptor
    time.sleep(15)  # Dejamos que se ejecute durante 5 segundos
    RUNNING = False  # Esto detendrá los bucles dentro de sender1 y receiver1
    sender_thread.join()  # Esperamos a que termine el hilo del emisor
    receiver_thread.join()  # Esperamos a que termine el hilo del receptor

# Punto de entrada principal
if __name__ == "__main__":
    print("Starting the stop and wait Protocol Simulation...")
    par_protocol()  # Llamamos a la función principal
    print("¡Simulation finished!")
    numero_entero = int(input("Por favor, ingresa un número entero: "))