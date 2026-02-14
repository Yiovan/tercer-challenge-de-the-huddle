import threading
import time

lista = []
bloqueo = threading.Lock()

def agregar(nombre):
    for i in range(5):
        with bloqueo:  # 🔒 sección crítica
            lista.append(f"{nombre}-{i}")
            print(f"{nombre} agregó {nombre}-{i}")
        time.sleep(0.1)

hilo1 = threading.Thread(target=agregar, args=("Hilo1",))
hilo2 = threading.Thread(target=agregar, args=("Hilo2",))

hilo1.start()
hilo2.start()

hilo1.join()
hilo2.join()

print("\nLista final:")
print(lista)
