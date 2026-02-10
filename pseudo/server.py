import socket #descargamos la libreria socket

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host= 'localhost'
puerto = 5000

servidor.bind((host,puerto))
servidor.listen(1)
print(f'servidor esperando en {host}:{puerto}...')

conexion, direccion = servidor.accept()
print('conectado')
while True:
    mensaje = conexion.recv(1024).decode('utf-8')
    print(f'cliente: {mensaje}')
    respuesta= input('mandale una respuesta de parte del servidor')
    if mensaje or respuesta in 'salir':
        break
    else:
        conexion.send(respuesta.encode('utf-8'))
        print(f'respuesta enviada: {respuesta}')

conexion.close()
servidor.close()
print('chau')