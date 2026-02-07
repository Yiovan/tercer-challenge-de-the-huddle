import socket
import selectors
import sys
import threading
import queue

sel = selectors.DefaultSelector()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 8081))
sock.setblocking(False)

sel.register(sock, selectors.EVENT_READ)

user_input_queue = queue.Queue()

def read_stdin_thread(q):
    while True:
        line = sys.stdin.readline()
        q.put(line)

stdin_thread = threading.Thread(target=read_stdin_thread, args=(user_input_queue,), daemon=True)
stdin_thread.start()

print("🟢 Conectado al chat. Escribí y presioná Enter.")

try:
    while True:
        # Procesar eventos del socket
        eventos = sel.select(1) # Timeout de 1 segundo
        for key, _ in eventos:
            if key.fileobj is sock:
                data = sock.recv(1024)
                if not data:
                    print("🔴 Servidor cerrado")
                    sys.exit()
                print(data.decode(), end="")
        
        # Procesar entrada del usuario de la cola
        try:
            msg = user_input_queue.get_nowait()
            if msg:
                sock.sendall(msg.encode())
        except queue.Empty:
            pass # No hay mensajes del usuario pendientes

except KeyboardInterrupt:
    print("\n👋 Saliendo del chat")
finally:
    sock.close()
    sys.exit(0) # Asegurarse de que el programa termine, incluyendo el hilo.

