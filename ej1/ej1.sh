#!/bin/bash
echo "Ejercicio 1"
python3 adder.py
rm ./VCD/adder.vcd
gtkwave ./VCD/adder.vcd
