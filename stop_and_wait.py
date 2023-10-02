# Importamos las clases y funciones del archivo Protocolo.py
from Protocolo import Frame, FrameKind, Packet, from_network_layer, to_physical_layer, wait_for_event, from_physical_layer, EventType, to_network_layer
import threading  # Importamos el módulo de hilos
import time  # Importamos el módulo de tiempo para pausas

RUNNING = True  # Una variable para controlar la ejecución
turnoS = True
turnoR = False
# Función del emisor
def sender2():
    flag = False
    global turnoS
    global turnoR
    while RUNNING:  # Mientras esté en ejecución
        if flag == False: 
            buffer = from_network_layer()  # Obtener algo para enviar desde la capa de red
            s = Frame()  # Crear un objeto frame
            s.info = buffer  # Copiamos el paquete en s para transmisión
            s.kind = FrameKind.DATA  # Set the frame kind as data
            print("Se envia el primer paquete")
            to_physical_layer(s)  # Enviamos el frame a la capa física
            flag = True
            turnoS = False
            turnoR = True
        else:
            if turnoS == True:
                event = wait_for_event()  # Esperamos un evento, la única posibilidad es la llegada de un frame
                print("recibe confirmacion")
                if event == EventType.FRAME_ARRIVAL:  # Si ha llegado un frame
                    buffer = from_network_layer()  # Obtener algo para enviar desde la capa de red
                    s = Frame()  # Crear un objeto frame
                    s.info = buffer  # Copiamos el paquete en s para transmisión
                    s.kind = FrameKind.DATA  # Set the frame kind as data
                    print("Se envia otro paquete")
                    to_physical_layer(s)  # Enviamos el frame a la capa física

                    flag = True
                    turnoS = False
                    turnoR = True
            else:
                pass

# Función del receptor
def receiver2():
    global turnoR
    global turnoS
    while RUNNING:  # Mientras esté en ejecución
        if turnoR:
            event = wait_for_event()  # Esperamos un evento, la única posibilidad es la llegada de un frame
            if event == EventType.FRAME_ARRIVAL:  # Si ha llegado un frame
                print("Se recive un paquete")
                r = from_physical_layer()  # Obtenemos el frame de la capa física
                to_network_layer(r.info)  # Enviamos la información del frame a la capa de red
                s = Frame()
                s.info = Packet("dummy!")  # Se envia un dummy para confirmarle al emisor
                print("Se envia dummy de confirmacion")
                to_physical_layer(s)
                turnoS = True
                turnoR = False
        else:
            pass

# Función principal del Protocolo Utopia
def stop_and_wait_protocol():
    global RUNNING  # Declaramos la variable global para modificarla posteriormente
    sender_thread = threading.Thread(target=sender2)  # Creamos un hilo para el emisor
    receiver_thread = threading.Thread(target=receiver2)  # Creamos un hilo para el receptor
    sender_thread.start()  # Iniciamos el hilo del emisor
    receiver_thread.start()  # Iniciamos el hilo del receptor
    time.sleep(5)  # Dejamos que se ejecute durante 5 segundos
    RUNNING = False  # Esto detendrá los bucles dentro de sender1 y receiver1
    sender_thread.join()  # Esperamos a que termine el hilo del emisor
    receiver_thread.join()  # Esperamos a que termine el hilo del receptor

# Punto de entrada principal
if __name__ == "__main__":
    print("Starting the stop and wait Protocol Simulation...")
    stop_and_wait_protocol()  # Llamamos a la función principal
    print("¡Simulation finished!")
    numero_entero = int(input("Por favor, ingresa un número entero: "))