#!/bin/bash
echo "Ejercicio 1"
rm ./VCD/adder.vcd
python3 adder.py
gtkwave ./VCD/adder.vcd
