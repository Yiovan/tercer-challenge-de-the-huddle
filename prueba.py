import socket

class Servidor:
    def __init__ (self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def servidor(self):
     
        self.server.bind(('localhost', 8080))
        self.server.listen(1)
        print(f'el servidor conectado es la direccion 8080')
        
    def cliente(self):
        cliente, self.cliente = self.server.accept()
        print(f"Cliente conectado desde {self.puerto}")

serv = Servidor()

while True:
    mensaje = serv.cliente.recv(1024).decode('utf-8')
    
    if not mensaje or mensaje.lower() == 'salir':
        print(f'cliente desconectado')
        break
    print(f'cliente: {mensaje}')
    
    respuesta = input('servidor: ')
    serv.cliente.send(respuesta.encode('utf-8'))
    
    
    if respuesta.lower("salir"):
        break

serv.cliente.close()
serv.server.close()
