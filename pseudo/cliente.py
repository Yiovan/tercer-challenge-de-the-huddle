import socket
import time


time.sleep(1)

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host= 'localhost'
puerto = 5000


print(f'inentando conectar al puerto {host}:{puerto}')
cliente.connect((host, puerto))
print("✅ Conectado al servidor!")
try:
    while True:
        mensaje_cliente= input('escribe tu mensaje: ')
        if mensaje_cliente in 'salir':
            break
        else:
            cliente.send(mensaje_cliente.encode('utf-8'))
            print(f'mensaje enviado {mensaje_cliente}')
        
        respuesta = cliente.recv(1024).decode('utf-8')
        print(f'servidor: {respuesta}')
except KeyboardInterrupt:
    cliente.close()
    print("👋 Conexión cerrada")
