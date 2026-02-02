import socket

# Crear socket y conectar
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('localhost', 8080))
print("Conectado al servidor")

while True:
    # ENVIAR mensaje al servidor
    mensaje = input("Tú: ")
    cliente.send(mensaje.encode('utf-8'))
    
    if mensaje.lower() == 'salir':
        break
    
    # RECIBIR respuesta del servidor
    respuesta = cliente.recv(1024).decode('utf-8')
    
    if not respuesta or respuesta.lower() == 'salir':
        print("Servidor desconectado")
        break
    
    print(f"Servidor: {respuesta}")

cliente.close()