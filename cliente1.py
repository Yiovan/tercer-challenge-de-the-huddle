import socket
import threading
import time

# ══════════════════════════════════════════
#  CONFIGURACIÓN
# ══════════════════════════════════════════
HOST = "localhost"
PORT = 8081
REINTENTOS_CONEXION = 5      # cuántas veces intenta conectarse al inicio
ESPERA_REINTENTO    = 3      # segundos entre cada intento
ESPERA_RECONEXION   = 5      # segundos antes de reconectarse si se cae a mitad

def recibir(sock, evento_caido):
 
    try:
        while True:
            datos = sock.recv(1024)
            if not datos:
                print("\n🔴 El servidor cerró la conexión")
                break
            print(datos.decode())
    except Exception:
        pass   # la conexión se cayó de golpe
    finally:
        evento_caido.set()   # ← le avisa al hilo principal que pasó algo

def conectar(nombre):
   
    for intento in range(1, REINTENTOS_CONEXION + 1):
        try:
            print(f" Intentando conectar... ({intento}/{REINTENTOS_CONEXION})")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
            sock.sendall(nombre.encode())   # primer mensaje = nombre
            print("✅ Conectado al servidor\n")
            return sock
        except ConnectionRefusedError:
            print(f"❌ Servidor no disponible. Reintentando en {ESPERA_REINTENTO}s...")
            sock.close()
            if intento < REINTENTOS_CONEXION:
                time.sleep(ESPERA_REINTENTO)

    print(" No se pudo conectar al servidor después de varios intentos.")
    return None




def iniciar_sesion(sock):
   
    evento_caido = threading.Event()


    hilo_receptor = threading.Thread( #crea el hilo, aun no hace nada 
        target=recibir, #recibe la funcion con el que va trabajar el hilo
        args=(sock, evento_caido), #le pasa la conexion a ESE 
        daemon=True
    )
    hilo_receptor.start()

    try:
        while True:

            # Si el hilo receptor detectó que la conexión se cayó,
            # salimos del loop para que main intente reconectarse.
            if evento_caido.is_set():
                print("\n⚠️  Conexión perdida. Intentando reconectar...")
                return False   # ← "no salí a propósito, reconéctame"

            msg = input()

            if evento_caido.is_set():
                # la conexión se fue justo mientras escribíamos
                print("⚠️  Conexión perdida al enviar. Intentando reconectar...")
                return False

            if msg.lower() == "salir":
                sock.sendall("/salir".encode())
                return True    # ← el usuario quiso salir

            sock.sendall(msg.encode())

    except KeyboardInterrupt:
        return True   # Ctrl+C = salida voluntaria
    except Exception:
        return False  # error de red = reconectar
    finally:
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        sock.close()



nombre = input("Escribe tu nombre: ").strip()
if not nombre:
    print("❌ El nombre no puede estar vacío")
    raise SystemExit

while True:
    sock = conectar(nombre)

    if sock is None:
        break   # agotó reintentos → salir

    salida_voluntaria = iniciar_sesion(sock)

    if salida_voluntaria:
        print("👋 Hasta luego")
        break

    # Si llegamos aquí es porque la conexión se cayó (no fue el usuario)
    print(f"🔁 Reconectando en {ESPERA_RECONEXION} segundos...")
    time.sleep(ESPERA_RECONEXION)