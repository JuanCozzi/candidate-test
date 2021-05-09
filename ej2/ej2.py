import re
import sys


in_file = open(sys.argv[1],"r")


if len(sys.argv)>2:
    out_file_name = ys.argv[2]
else: 
    out_file_name = "fix_" + sys.argv[1]

out_file = open(out_file_name, "w+")


i = 0
new_verilog = in_file.read()

patron = re.compile(r"(  reg \[(.*)\] (\S*) \[(.*)\];\n)*  initial begin\n((    \S*\[\S*\] = \S*;\n)*)  end\n")
result = patron.search(new_verilog)

while result:
    info = result.groups()
    mem_name = info[2]
    mem_file_name = "memdump"+ str(i) + ".mem"
    mem_file = open(mem_file_name,"w+")


    remplace = info[0] +"  $readmemh(\"" + mem_file_name + "\", " + mem_name + ");\n"

    print(result.group())
    print(result.groups())


    mem_numbers = re.findall(r"= 8'h(\w*);", info[4])

    for numbers in mem_numbers:
        mem_file.write(numbers +"\n")

    new_verilog = new_verilog[0:result.start()] + remplace + new_verilog[result.end() ::]

    patron = re.compile(r"(  reg \[(.*)\] (\S*) \[(.*)\];\n)*  initial begin\n((    \S*\[\S*\] = \S*;\n)*)  end\n")
    result = patron.search(new_verilog)

    i += 1



print("Se modificaron: " + str(i) + "sintaxis")

out_file.write(new_verilog)
