## EXPLICACION DE COMO ESTA ESTRUCTURADO EL SERVIDOR



```
import socket
import threading
```


se importan las librerias para hacer un socket y los multiples conectores con hilos


```
clientes = {}
```

se usa un diccionario para identificar cada cliente con una id 