from protocolo import *

MAX_SEQ = 7  # Define una constante para el número máximo de secuencia.

# Función que determina si un número se encuentra en un rango circular.
def between(a, b, c):
    # Los números son tratados como si estuvieran en un círculo, y esta función determina si b está entre a y c en ese círculo.
    return ((a <= b) < c) or ((c < a) <= b) or ((b < c) < a)

# Función que envía datos.
def send_data(frame_nr, frame_expected, buffer):
    s = Frame()  # Crea un nuevo marco.
    s.info = buffer[frame_nr]  # Carga el marco con datos del buffer.
    s.seq = frame_nr  # Establece el número de secuencia del marco.
    s.ack = (frame_expected + MAX_SEQ) % (MAX_SEQ + 1)  # Establece el número de reconocimiento (ack) del marco.
    to_physical_layer(s)  # Envía el marco a la capa física.
    start_timer(frame_nr)  # Inicia un temporizador para este marco.

# Función principal del protocolo 5.
def protocol5():
    next_frame_to_send = 0  # Establece el número del próximo marco a enviar.
    ack_expected = 0  # Establece el número del próximo ack esperado.
    frame_expected = 0  # Establece el número del próximo marco esperado.
    buffer = [None for _ in range(MAX_SEQ + 1)]  # Crea un buffer para almacenar marcos.
    nbuffered = 0  # Inicializa el número de marcos en el buffer a 0.

    enable_network_layer()  # Habilita la capa de red para enviar paquetes.

    # Bucle principal del protocolo.
    while True:
        event = wait_for_event("go_back_n")  # Espera un evento.
        
        # Si la capa de red está lista para enviar un paquete.
        if event == EventType.NETWORK_LAYER_READY:
            buffer[next_frame_to_send] = from_network_layer()  # Recupera un paquete de la capa de red y lo almacena en el buffer.
            nbuffered += 1  # Incrementa el número de paquetes en el buffer.
            send_data(next_frame_to_send, frame_expected, buffer)  # Envía el paquete.
            next_frame_to_send = (next_frame_to_send + 1) % (MAX_SEQ + 1)  # Incrementa el número del próximo marco a enviar.
        
        # Si se ha recibido un marco.
        elif event == EventType.FRAME_ARRIVAL:
            r = from_physical_layer()  # Recupera el marco de la capa física.
            
            # Si el número de secuencia del marco coincide con el esperado.
            if r.seq == frame_expected:
                to_network_layer(r.info)  # Envia la información del marco a la capa de red.
                frame_expected = (frame_expected + 1) % (MAX_SEQ + 1)  # Incrementa el número del próximo marco esperado.
            
            # Mientras el ack esperado esté entre el ack del marco recibido y el próximo marco a enviar.
            while between(ack_expected, r.ack, next_frame_to_send):
                nbuffered -= 1  # Decrementa el número de paquetes en el buffer.
                stop_timer(ack_expected)  # Detiene el temporizador para este ack.
                ack_expected = (ack_expected + 1) % (MAX_SEQ + 1)  # Incrementa el número del próximo ack esperado.

        # Si el marco tiene un error de suma de verificación, simplemente lo ignora.
        elif event == EventType.CKSUM_ERR:
            pass

        # Si se ha producido un tiempo de espera.
        elif event == EventType.TIMEOUT:
            next_frame_to_send = ack_expected  # Restablece el número del próximo marco a enviar al ack esperado.
            for i in range(1, nbuffered + 1):  # Para cada paquete en el buffer.
                send_data(next_frame_to_send, frame_expected, buffer)  # Reenvía el paquete.
                next_frame_to_send = (next_frame_to_send + 1) % (MAX_SEQ + 1)  # Incrementa el número del próximo marco a enviar.
        
        # Si el número de paquetes en el buffer es menor que MAX_SEQ, habilita la capa de red.
        if nbuffered < MAX_SEQ:
            enable_network_layer()
        else:  # De lo contrario, la deshabilita.
            disable_network_layer()

def to_physical_layer(frame):
    pass

def start_timer(seq_nr):
    pass

def enable_network_layer():
    pass

def from_network_layer():
    pass

def disable_network_layer():
    pass

def from_physical_layer():
    pass

def stop_timer(seq_nr):
    pass

def to_network_layer(info):
    pass
