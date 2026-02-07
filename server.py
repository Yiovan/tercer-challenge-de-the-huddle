import socket
import selectors

sel = selectors.DefaultSelector()
clientes = {}
PUERTO = 8081
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", PUERTO))
server.listen()
server.setblocking(False)

sel.register(server, selectors.EVENT_READ)
print(f"🟢 Servidor de chat escuchando en {PUERTO}")

def broadcast(mensaje, origen=None):
    for sock in list(clientes):
        if sock != origen:
            try:
                sock.sendall(mensaje)
            except OSError:
                desconectar(sock)

def desconectar(sock):
    addr = clientes.get(sock, "desconocido")
    print(f"🔴 Cliente desconectado: {addr}")
    sel.unregister(sock)
    sock.close()
    clientes.pop(sock, None)
    broadcast(f"[SERVIDOR] {addr} salió del chat\n".encode())

try:
    while True:
        eventos = sel.select(1)

        for key, _ in eventos:
            if key.fileobj is server:
                cliente, addr = server.accept()
                cliente.setblocking(False)
                sel.register(cliente, selectors.EVENT_READ)
                clientes[cliente] = addr
                print(f"🟢 Cliente conectado: {addr}")
                broadcast(f"[SERVIDOR] {addr} entró al chat\n".encode())

            else:
                sock = key.fileobj
                try:
                    data = sock.recv(1024)
                    if not data:
                        desconectar(sock)
                    else:
                        mensaje = f"{clientes[sock]}: ".encode() + data
                        broadcast(mensaje, origen=sock)

                except OSError:
                    desconectar(sock)

except KeyboardInterrupt:
    print("\n🛑 Cerrando servidor...")
    for sock in list(clientes):
        sock.close()
    server.close()
