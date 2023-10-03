from protocolo import *  # Importa todas las funciones y clases del módulo Protocolo

MAX_SEQ = 1  # Define una constante para la máxima secuencia, que en este caso es 1 debido al protocolo de ventana deslizante de 1 bit

# Función que simula la máquina A
def protocol_machineA():
    next_frame_to_send = 0  # Inicializa el próximo frame a enviar
    frame_expected = 0  # Inicializa el frame que espera recibir
    buffer = from_network_layer()  # Obtiene un paquete desde la capa de red para enviar

    s = Frame()  # Crea un nuevo frame
    s.info = buffer  # Inserta el paquete en el frame
    s.seq = next_frame_to_send  # Establece el número de secuencia del frame
    s.ack = 1 - frame_expected  # Establece el número de acuse de recibo, que es el inverso del frame esperado

    to_physical_layer_from_A(s)  # Envía el frame a la capa física
    start_timer_sliding(5, timeout_handler)  # Inicia un temporizador con un intervalo de 5 segundos y una función de manejo de tiempo agotado

    # Bucle infinito para continuar enviando y recibiendo frames
    while True:
        tiempo_inicial = datetime.now()  # Obtiene la hora actual
        event = wait_for_event_par(tiempo_inicial)  # Espera un evento, que puede ser la llegada de un frame, un error de suma de comprobación o un tiempo agotado
        
        # Si se recibe un frame
        if event == EventType.FRAME_ARRIVAL:
            r = from_physical_layer_at_A()  # Obtiene el frame de la capa física
            
            if r is None:  # Si no se recibió ningún frame, continua con la siguiente iteración del bucle
                continue

            # Si el número de secuencia del frame recibido es el esperado
            if r.seq == frame_expected:
                to_network_layer(r.info)  # Envía el paquete del frame a la capa de red
                frame_expected = 1 - frame_expected  # Invierte el número de secuencia esperado
            
            # Si el número de acuse de recibo es el esperado
            if r.ack == next_frame_to_send:
                stop_timer(tiempo_inicial)  # Detiene el temporizador
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
        
        to_physical_layer_from_A(s)  # Envía el frame a la capa física
        start_timer_sliding(5, timeout_handler)  # Reinicia el temporizador

def protocol_machineB():
    # Inicializa el próximo frame a enviar
    next_frame_to_send = 0  
    
    # Inicializa el frame que espera recibir
    frame_expected = 0  
    
    # Obtiene un paquete desde la capa de red para enviar
    buffer = from_network_layer()  

    # Crea un nuevo frame
    s = Frame()
    
    # Inserta el paquete en el frame
    s.info = buffer  
    
    # Establece el número de secuencia del frame
    s.seq = next_frame_to_send  
    
    # Establece el número de acuse de recibo, que es el inverso del frame esperado
    s.ack = 1 - frame_expected  

    # Envía el frame a la capa física
    to_physical_layer_from_B(s)
    
    # Inicia un temporizador con un intervalo de 5 segundos y una función de manejo de tiempo agotado
    start_timer_sliding(5, timeout_handler)  

    # Bucle infinito para continuar enviando y recibiendo frames
    while True:
        # Obtiene la hora actual
        tiempo_inicial = datetime.now()
        
        # Espera un evento, que puede ser la llegada de un frame, un error de suma de comprobación o un tiempo agotado
        event = wait_for_event_par(tiempo_inicial)

        # Si se recibe un frame
        if event == EventType.FRAME_ARRIVAL:
            # Obtiene el frame de la capa física
            r = from_physical_layer_at_B()
            
            # Si no se recibió ningún frame, continua con la siguiente iteración del bucle
            if r is None:  
                continue

            # Si el número de secuencia del frame recibido es el esperado
            if r.seq == frame_expected:
                # Envía el paquete del frame a la capa de red
                to_network_layer(r.info)
                
                # Invierte el número de secuencia esperado
                frame_expected = 1 - frame_expected

            # Si el número de acuse de recibo es el esperado
            if r.ack == next_frame_to_send:
                # Detiene el temporizador
                stop_timer(tiempo_inicial)
                
                # Obtiene un nuevo paquete desde la capa de red para enviar
                buffer = from_network_layer()
                
                # Invierte el número de secuencia a enviar
                next_frame_to_send = 1 - next_frame_to_send

        # Si ocurre un error de suma de comprobación
        elif event == EventType.CKSUM_ERR:
            # Imprime un mensaje de error
            print("B: Checksum Error!")

        # Prepara el próximo frame a enviar
        s.info = buffer
        s.seq = next_frame_to_send
        s.ack = 1 - frame_expected
        
        # Envía el frame a la capa física
        to_physical_layer_from_B(s)
        
        # Reinicia el temporizador
        start_timer_sliding(5, timeout_handler) 

# Si este script es el módulo principal
if __name__ == "__main__":
    # Inicia un hilo para simular la máquina A
    threading.Thread(target=protocol_machineA).start()  
    
    # Inicia un hilo para simular la máquina B
    threading.Thread(target=protocol_machineB).start()  