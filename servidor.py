import socket
import threading

clientes = {}
bloqueos = threading.Lock() #se genera un candado

def broadcast(mensaje, omitir=None):
    mensaje_bytes = mensaje.encode()
    with bloqueos: #es un candado para que dos hilos no toquen lo mismo al mismo tiempo.
        conexiones = list(clientes.keys()) #

    for conexion in conexiones:
        if conexion != omitir: 
            try:
                conexion.sendall(mensaje_bytes)
            except (OSError, ConnectionResetError):  
                with bloqueos:
                    if conexion in clientes:
                        del clientes[conexion]
                conexion.close()
             #lo que hace es que envia a todos el mensaje y despues

def manejar_cliente(conexion, direccion):
    try:
        # El primer mensaje que recibimos será el nombre
        nombre = conexion.recv(1024).decode().strip()
        
        with bloqueos: clientes[conexion] = nombre
        
        print(f"🟢 {nombre} se ha unido desde {direccion}")
        broadcast(f"📢 {nombre} ha entrado al chat")

        while True:
            datos = conexion.recv(1024)
            if not datos: break
            
            texto = datos.decode().strip()

            if texto == "/salir":
                print(f"🔴 {nombre} solicitó salir")
                break

            mensaje_formateado = f"{nombre}: {texto}"
            print(mensaje_formateado)
            broadcast(mensaje_formateado, omitir=conexion)


    except Exception as e:
        print(f"❌ Error con cliente: {e}")

    finally:
        nombre_salir = None

        with bloqueos:
            if conexion in clientes:
                nombre_salir = clientes[conexion]
                del clientes[conexion]

        if nombre_salir:
            broadcast(f"🔴 {nombre_salir} ha salido")

        conexion.close()

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
servidor.bind(('localhost', 8081))
servidor.listen()
servidor.settimeout(1)


print("Servidor esperando nombres en puerto 8081")

try:
    while True:
        try:
            conexion, direccion = servidor.accept()
        except:
            continue
        threading.Thread( #crea el hilo
            target=manejar_cliente, #llama a la funcion que va usar 
            args=(conexion, direccion),  
            daemon=True
            ).start()
except KeyboardInterrupt:
    print("\nServidor apagado y/o caido")
finally:
    servidor.close()