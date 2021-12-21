# Trabajo Practico 2 - Openflow Lite

Este trabajo practico consistio en generar una topología usando mininet sobre la cual se realizaran diferentes ensayos. 

Tambien pidió implementar un Firewall usando POX con las siguientes reglas definida:

1. Se deben descartar todos los mensajes cuyo puerto destino sea 80.
2. Se deben descartar todos los mensajes que provengan del host 1, tengan como puerto destino el 5001, y esten
utilizando el protocolo UDP.
3. Se debe elegir dos hosts cualquiera, y los mismos no deben poder comunicarse de ninguna forma

## Levantando el Firewall

Antes de levantar la topología, se debe levantar el Firewall de la siguiente forma:

```
$ python3 pox.py log.level --DEBUG openflow.of_01 forwarding.l2_learning controlador
```

## Levantando la topología

Una vez levantado el Firewall, se debera correr el siguiente comando en otra consola para levantar la topología:

```
$ sudo mn --custom ./topologia.py --topo tp2,switches=2 --mac --arp --switch ovsk --controller remote
```

Es importante que luego del parámetro --custom se ponga la ubicación del archivo de la topología.

Para especificar la cantidad de switches luego del parametro `--topo tp2,..` despues de la coma se debe ingresar la cantidad de switches que se desee tener, el ejemplo mostrado creará 2 switches.

## Pruebas
Una vez levantado el Firewall y la topología para probar el correcto funcionamiento de ambos se pueden hacer las siguiente pruebas:

### Regla 1

Esta regla indica que se deberán descartar todos los mensajes cuyo puerto destino sea 80. 

Para probar esta regla seguimos los siguientes pasos:

1. Abrir 2 terminales para hosts distintos desde mininet con el comando `xterm`, pueden ser cualquiera.

```
mininet> xterm host_3
mininet> xterm host_4
```

2. En una de esas terminales usar el comando `iperf` en modo server en el puerto 80:

```
# iperf -s -p 80
```

3. En la otra terminal usar el comando `iperf` en modo client con la dirección IP del server (10.0.0.X) en este caso suponiendo que el server fue levantado en el host 3 la direccion IP sería 10.0.0.3:

```
# iperf -c 10.0.0.3 -t 1
```

4. El resultado debería ser el siguiente:
```
# iperf -c 10.0.0.3
connect failed: Connection refused
```

### Regla 2

Esta regla indica que se deberán descartar todos los mensajes que provengan del host 1, tengan como puerto destino el 5001, y estén utilizando el protocolo UDP. 

Para probar esta regla seguimos los siguientes pasos:

1. Abrir 2 terminales para hosts distintos desde mininet con el comando `xterm`, entre estas debe estar el host 1.

```
mininet> xterm host_1
mininet> xterm host_4
```

2. En la terminal que no sea del host 1 usar el comando `iperf` en modo server UDP con el puerto 5001:

```
# iperf -s -p 5001 -u
```

1. En la terminal del host 1 usar el comando `iperf` en modo client UDP con la dirección IP del server en este caso 10.0.0.4, en el puerto 5001:

```
# iperf -c 10.0.0.4 -u -p 5001 -t 1
```

4. El resultado debería ser el siguiente:

```
# iperf -c 10.0.0.4 -u -p 5001 -t 1
------------------------------------------------------------
Client connecting to 10.0.0.4 UDP port 5001
Sending 1470 byte datagrams, IPG target: 11215.21 us (kalman adjust)
UDP buffer size: 208 KByte (default)
------------------------------------------------------------
[ 25] local 10.0.0.1 port 47573 connected with 10.0.0.4 port 5001
[ 25] WARNING: did not receive ack of last datagram after 10 tries.
[ ID] Interval       Transfer     Bandwidth
[ 25]  0.0-10.0 sec  1.25 MBytes  1.05 Mbits/sec
[ 25] Sent 892 datagrams
```

### Regla 3

Esta regla indica que se deberá restringir completamente la comunicación entre los hosts 1 y 2, bloqueando todo tipo de tráfico entre estos.

Para probar esta ultima regla seguimos los siguientes pasos:

1. Ejecutar el comando pingall en mininet

```
mininet> pingall
```

2. El resultado debería ser el siguiente:

```
*** Ping: testing ping reachability
host_1 -> X host_3 host_4 
host_2 -> X host_3 host_4 
host_3 -> host_1 host_2 host_4 
host_4 -> host_1 host_2 host_3 
*** Results: 16% dropped (10/12 received)
```