# Importamos las clases y funciones del archivo Protocolo.py
from protocolo import Frame, FrameKind, Packet, from_network_layer, to_physical_layer, wait_for_event, from_physical_layer, EventType, to_network_layer
turnoS = True
turnoR = False
flag = False
# Función del emisor
def sender(socketio):
    global flag
    global turnoS
    global turnoR
    if flag == False: 
        buffer = from_network_layer()  # Obtener algo para enviar desde la capa de red
        s = Frame()  # Crear un objeto frame
        s.info = buffer  # Copiamos el paquete en s para transmisión
        s.kind = FrameKind.DATA  # Set the frame kind as data
        print("Se envia el primer paquete")
        to_physical_layer(s,socketio)  # Enviamos el frame a la capa física
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
                to_physical_layer(s,socketio)  # Enviamos el frame a la capa física
                flag = True
                turnoS = False
                turnoR = True

# Función del receptor
def receiver(socketio):
    global turnoR
    global turnoS
    if turnoR:
        event = wait_for_event()  # Esperamos un evento, la única posibilidad es la llegada de un frame
        if event == EventType.FRAME_ARRIVAL:  # Si ha llegado un frame
            print("Se recive un paquete")
            r = from_physical_layer(socketio)  # Obtenemos el frame de la capa física
            to_network_layer(r.info,socketio)  # Enviamos la información del frame a la capa de red
            s = Frame()
            s.info = Packet("dummy!")  # Se envia un dummy para confirmarle al emisor
            print("Se envia dummy de confirmacion")
            to_physical_layer(s,socketio)
            turnoS = True
            turnoR = False