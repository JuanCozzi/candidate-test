import re
import sys
import argparse

PATTERN = re.compile(r'(  reg \[(.*)\] (\S*) \[(.*)\];\n)*  initial begin\n((    \S*\[\S*\] = \S*;\n)*)  end\n')


def fix_file(file_contents, out_file):
    '''
        This function looks for the unsupported syntax 
    type in the file_contents string and sets the correct syntax by creating
    a .mem file for each memory record it finds. The inputs are the string 
    file_contents and the name of the output file.
    '''

    # Number of memories
    i = 0 

    result = PATTERN.search(file_contents)

    while result:
        info = result.groups()
        mem_name = info[2]
        mem_file_name = 'memdump' + str(i) + '.mem'

        fixed_syntax = info[0] + '  $readmemh(\"' + mem_file_name + '\", ' + mem_name + ');\n'
        
        # Search for the initial values of the memory
        mem_values = re.findall(r"= 8'h(\w*);", info[4])

        with open(mem_file_name,'w+') as mem_file:
            for value in mem_values:
                mem_file.write(value + '\n')

        file_contents = file_contents[0:result.start()] + fixed_syntax + file_contents[result.end() ::]
        result = PATTERN.search(file_contents)
        i += 1

    print(f'Modified memory blocks number: {i}')

    with open(out_file_name, 'w') as out_file:
        out_file.write(file_contents) 


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='EJ:2 This script is responsible for modifying the nmigen output file by changing the syntax type of memory initializations. ')
    parser.add_argument('--in_file', default = 'testcase.v', 
    help = 'Enter the in file name with its extension, default case \"testcase.v\"')
    parser.add_argument('--out_file',help = 'Enter the out file name with its extension, default case \"fixed_IN_FILE\"')

    args = parser.parse_args()

    out_file_name = args.out_file

    if out_file_name is None:
        out_file_name = 'fixed_' + args.in_file

    with open(args.in_file, 'r') as in_file:
        file_contents = in_file.read()

    fix_file(file_contents, out_file_name)
