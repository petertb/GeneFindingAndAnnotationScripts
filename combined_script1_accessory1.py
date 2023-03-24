#!/bin/python

#-----import
import sys

#-----variables (passed from shell script)
genome_assembly_file1 = sys.argv[1]
#note that number of splits is 2 less than the number of cores
num_splits = int(sys.argv[2]) - 2
output_folder = sys.argv[3]

#-----import genome assembly
with open(genome_assembly_file1, 'r') as f:
    file1 = f.readlines()

#-----count number of lines in fasta file
total_lines = len(file1)

#-----calculate minimum lines in each new fasta file
min_lines_per_split = int(round(total_lines/num_splits, 0))
#print(min_lines_per_split)

#-----iterate through file and create splits
line_count1 = 0
file_count = 0
line_list1 = []

for row1 in file1:
    if row1[0] == '>':
        if line_count1 > min_lines_per_split:
            name_of_split1 = str(output_folder) + genome_assembly_file1.replace('.fasta', '') + '_' + str(file_count) + '.fasta'
            with open(name_of_split1, 'w') as g:
                for item1 in line_list1:
                    g.write(item1)
            line_list1 = []
            line_list1.append(row1)
            line_count1 = 0
            file_count += 1
        else:
            line_list1.append(row1)
            line_count1 += 1
    else:
        line_list1.append(row1)
        line_count1 += 1

#output final split saved in line_list1 variable
name_of_split1 = str(output_folder) + genome_assembly_file1.replace('.fasta', '') + '_' + str(file_count) + '.fasta'
with open(name_of_split1, 'w') as g:
    for item1 in line_list1:
        g.write(item1)
