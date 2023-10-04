# Importamos las clases y funciones del archivo protocolo.py
from protocolo import *
turnoS = True
turnoR = False
flag = False
# Función del emisor
def sender(socketio,error,___secuencia):
    global flag
    global turnoS
    global turnoR
    if flag == False: 
        buffer = from_network_layer()  # Obtener algo para enviar desde la capa de red
        s = Frame()  # Crear un objeto frame
        s.info = buffer  # Copiamos el paquete en s para transmisión
        s.kind = FrameKind.DATA  # Set the frame kind as data
        print("Se envia el primer paquete")
        to_physical_layer(s,socketio,"A")  # Enviamos el frame a la capa física
        flag = True
        turnoS = False
        turnoR = True
    else:
        if turnoS == True:
            print("recibe confirmacion")
            event = wait_for_event(error,"stop_and_wait")  # Esperamos un evento, la única posibilidad es la llegada de un frame
            from_physical_layer(socketio,"A")  # Obtenemos el frame de la capa física
            if event == EventType.FRAME_ARRIVAL:  # Si ha llegado un frame
                buffer = from_network_layer()  # Obtener algo para enviar desde la capa de red
                s = Frame()  # Crear un objeto frame
                s.info = buffer  # Copiamos el paquete en s para transmisión
                s.kind = FrameKind.DATA  # Set the frame kind as data
                print("Se envia otro paquete")
                to_physical_layer(s,socketio,"A")  # Enviamos el frame a la capa física
                flag = True
                turnoS = False
                turnoR = True
            

# Función del receptor
def receiver(socketio,error,___secuencia):
    global turnoR
    global turnoS
    if turnoR:
        event = wait_for_event(error,"stop_and_wait")  # Esperamos un evento, la única posibilidad es la llegada de un frame
        if event == EventType.FRAME_ARRIVAL:  # Si ha llegado un frame
            print("Se recive un paquete")
            r = from_physical_layer(socketio,"B")  # Obtenemos el frame de la capa física
            to_network_layer(r.info,socketio,"B")  # Enviamos la información del frame a la capa de red
            s = Frame()
            s.info = Packet("dummy!")  # Se envia un dummy para confirmarle al emisor
            print("Se envia dummy de confirmacion")
            print(s)
            to_physical_layer(s,socketio,"B")
            turnoS = True
            turnoR = False