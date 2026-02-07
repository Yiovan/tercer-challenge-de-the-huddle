import socket
import selectors
import sys

sel = selectors.DefaultSelector()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 8080))
sock.setblocking(False)

sel.register(sock, selectors.EVENT_READ)
sel.register(sys.stdin, selectors.EVENT_READ)

print("🟢 Conectado al chat. Escribí y presioná Enter.")

try:
    while True:
        eventos = sel.select()

        for key, _ in eventos:
            if key.fileobj is sock:
                data = sock.recv(1024)
                if not data:
                    print("🔴 Servidor cerrado")
                    sys.exit()
                print(data.decode(), end="")

            else:
                msg = sys.stdin.readline()
                sock.sendall(msg.encode())

except KeyboardInterrupt:
    print("\n👋 Saliendo del chat")
    sock.close()
