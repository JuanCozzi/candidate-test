# Ejercicio #1

El ejercicio consiste en desarrollar y simular un sumador con lógica de números signados complemento a 2 que cumpla con la siguiente interfaz:

```
           |--------------|
 a_data -->|              |
a_valid -->|              |
a_ready <--|              |
           |              |-->  r_data
           |    Adder     |--> r_valid
           |              |<--  r_ready
 b_data -->|              |
b_valid -->|              |
b_ready <--|              |
           |--------------|
               ^       ^
               |       |
              rst     clk
```


* **Ejecución del script**

El script encargado del ejercicio se llama (`adder.py`) y se deberá ejecutar de la sigiente manera: 

```
python3 adder.py  
```
El mismo devolverá un archivo `adder.vcd` correspondiente a la simulación en la carpeta `./VCD/`. Para ejecutar el script junto
a la simulación se deberá usar los siguientes comandos:

```
chmod +x ej1.sh
./ej1.sh 
```


* **Especificaciones del sumador**

Tanto las dos entradas como la salida cumplen un protocolo genérico stream con las
siguientes características:

* Las señales `_data` tienen N bits definidas durante la instanciación.
* La cantidad de bits de `r_data` es igual a la cantidad de bits de la señal de entrada. 
* El dato `_data` es leído por el sumidero cuando `_valid` y `_ready` están en 1.
* La señal `_valid` no depende de la señal `_ready` del mismo puerto para ir a 1.

Todas los datos que salgan por el puerto `r` son el resultado valido entre los datos
del puerto `a` y puerto `b`. No se realizar corroboración de overflow.



* **Herramientas utilizadas**

* [nMigen](https://nmigen.info/nmigen/latest/) para su desarrollo.
* [cocotb](https://docs.cocotb.org/en/stable/) para su testeo.
* [iverilog](http://iverilog.icarus.com/) para la simulación.
* [GTKWave](http://gtkwave.sourceforge.net/) para visualizar la simulación.
