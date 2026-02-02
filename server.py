import socket

# Crear socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8080))
server.listen(1)
print("Servidor esperando conexiones...")

# Aceptar conexión
cliente, direccion = server.accept()
print(f"Cliente conectado desde {direccion}")

while True:
    # RECIBIR mensaje del cliente
    mensaje = cliente.recv(1024).decode('utf-8')
    
    if not mensaje or mensaje.lower() == 'salir':
        print("Cliente desconectado")
        break
    
    print(f"Cliente: {mensaje}")
    
    # ENVIAR respuesta al cliente
    respuesta = input("Tú: ")
    cliente.send(respuesta.encode('utf-8'))
    
    if respuesta.lower() == 'salir':
        break

cliente.close()
server.close()