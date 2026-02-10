# Chat TCP con Python

Este proyecto implementa un chat simple usando sockets TCP, selectors y hilos, permitiendo múltiples clientes conectados al mismo tiempo desde la terminal. Todo funciona con texto crudo y en tiempo real.

## Archivos

* `server.py` → Servidor TCP, maneja múltiples clientes y broadcast.
* `client.py` → Cliente TCP, permite enviar y recibir mensajes en tiempo real.
* `README.md` → Explicación de conceptos y funcionamiento.

## Conceptos usados y relacionados

### 1. Socket

Un socket es un punto de comunicación entre dos máquinas en una red.

* Permite enviar y recibir datos.
* Cada socket se identifica con una IP y un puerto.
* En TCP, los sockets son confiables: los datos llegan completos y en orden.

Ejemplo en Python:

```python
socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

### 2. IPv4 e IPv6

* **IPv4**: Direcciones de 32 bits (ej. `192.168.0.1`)
* **IPv6**: Direcciones de 128 bits (ej. `2001:0db8::1`)
* Este proyecto usa IPv4 (`AF_INET`), pero se podría usar IPv6 (`AF_INET6`) para redes más grandes.

### 3. Hilos (Threads)

* Permiten ejecutar varias tareas simultáneamente en el mismo programa.
* En el cliente usamos un hilo daemon para leer la entrada del usuario sin bloquear el loop principal.
* `daemon=True` → el hilo termina automáticamente al cerrar el programa.

### 4. Selectores

* Permiten monitorear múltiples sockets sin bloquear el programa.
* `sel.select(timeout)` devuelve los sockets listos para leer o escribir.
* Esto permite un servidor que atiende muchos clientes sin crear un hilo por cliente.

### 5. Broadcast

* Enviar un mensaje a todos los clientes conectados.
* El servidor recibe un mensaje de un cliente y lo reenvía a los demás.
* Se evita que el mensaje se reenvíe al propio emisor (opcional).

### 6. Manejo de desconexiones

* Si un cliente se desconecta inesperadamente:
  * `recv()` devuelve vacío → cliente cerrado
  * `OSError` o `ConnectionResetError` → socket muerto
* Se elimina del diccionario de clientes y del selector para no romper el servidor.

### 7. Por qué si no pasa algo no se puede cerrar el servidor

* Los sockets en modo bloqueante (`blocking=True`) esperan indefinidamente en `accept()` o `recv()`.
* Para poder cerrar el servidor de forma limpia:
  * Usamos selectores con timeout → revisan periódicamente si deben cerrarse.
  * Esto permite capturar `KeyboardInterrupt` y cerrar todos los sockets correctamente.

## Alternativas de implementación

* **Hilos por cliente**: cada cliente tiene su propio hilo. Más simple, pero menos escalable.
* **Asyncio**: manejo asíncrono sin hilos ni selectores. Más moderno y eficiente para muchos clientes.
* **WebSockets**: protocolo para chat en navegadores, bidireccional y persistente.

## Cómo usar

1. Ejecutar el servidor:

```bash
python server.py
```

2. Ejecutar uno o más clientes:

```bash
python client.py
```

3. Escribir mensajes en cualquier cliente y verlos reflejados en todos los demás.

4. Ctrl+C para salir de servidor o cliente.