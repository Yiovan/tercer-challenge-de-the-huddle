import socket
import threading

def recibir(sock):
    try:
        while True:
            datos = sock.recv(1024)
            if not datos:
                print("🔴 Conexión cerrada por el servidor")
                break
            print(datos.decode())
    except Exception as e:
        print(f"❌ Error al recibir: {e}")
    finally:
        sock.close()

# ===== CLIENTE =====

nombre = input("Escribe tu nombre: ").strip()
if not nombre:
    print("❌ El nombre no puede estar vacío")
    raise SystemExit

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 8081))

# Enviar nombre apenas conecta
sock.sendall(nombre.encode())

# Hilo receptor
threading.Thread(target=recibir, args=(sock,), daemon=True).start()

try:
    while True:
        msg = input()
        if msg.lower() == "salir":
            sock.sendall("/salir".encode())
            break

        sock.sendall(msg.encode())
except KeyboardInterrupt:
    pass
finally:
    try:
        sock.shutdown(socket.SHUT_RDWR)
    except:
        pass
    sock.close()
