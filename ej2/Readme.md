# Ejercicio #2

El ejercicio consiste en desarrollar un script que realice una adaptación de la sintaxis de verilog generada
por el output de [nMigen](https://nmigen.info/nmigen/latest/). Puntualmente la inicialización inline de memorias. 




* **Ejecución del script**

El script encargado del ejercicio se llama (`ej2.py`) y se deberá ejecutar de la sigiente manera: 

```
python3 ej2.py --in_file v_file_in.v  --out_file v_file_out.v 
```

Siendo `v_file_in.v` y `v_file_out.v`definidos por el usuario. En el caso de no ingresar el nombre de archivo de entrada, utilizará el nombre por defecto `testcase.v` y si no se ingresa el nombre de archivo de salida, se utilizará el nombre del archivo original anteseguido del prefijo fix_, dando por resultado `fix_v_file_in.v`.




* **Generación del archivo verilog**


Para realizar una prueba del ejercicio es necesario obtener el output file generado por la herramienta nMigen, para 
ello se deberá ejecutar la siguiente linea:

```
python3 generate.py generate v_file_in.v
```

Una vez ejecutado el script del ejercicio, este generará un archivo `v_file_out.v` con la sintaxis soportada y otros archivos `memdump0.mem` correspondientes a los datos de inicialización de las memorias. Se generarán la cantidad de archivos `memdump0.mem` de acuerdo a la cantidad de inicializaciones de memoria posea el `v_file_in.v` siendo flexible en el nombre que se le otorge. 



* **Sintaxis no soportada**
```verilog
  reg [7:0] mem [15:0];
  initial begin
    mem[0] = 8'h3d;
    mem[1] = 8'hc9;
    mem[2] = 8'hbf;
    mem[3] = 8'hd5;
    mem[4] = 8'h52;
    mem[5] = 8'he0;
    mem[6] = 8'h05;
    mem[7] = 8'hc8;
    mem[8] = 8'hbc;
    mem[9] = 8'h6e;
    mem[10] = 8'h98;
    mem[11] = 8'h9f;
    mem[12] = 8'h4b;
    mem[13] = 8'h4c;
    mem[14] = 8'h39;
    mem[15] = 8'h55;
  end
```



* **Sintaxis soportada**
```verilog
  reg [7:0] mem [15:0];
  $readmemh("memdump0.mem", mem);
```
**memdump0.mem**:
```
3d
c9
bf
d5
52
e0
05
c8
bc
6e
98
9f
4b
4c
39
55
```



