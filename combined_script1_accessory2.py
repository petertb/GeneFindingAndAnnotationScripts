#!/bin/python

#-----import
import sys

#-----variables (passed from shell script)
#this variable is an array and should be saved as a python list
augustus_output_file_list1 = sys.argv[2:]
output_filename1 = 'Augustus_protein_sequences'
#header tag for each fasta document
unique_name1 = str(sys.argv[1])

#-----read in list of Augustus output files and concatenate
#declare empty list variable for reading files into
file1 = []
#read each output file into file1 list
for item1 in augustus_output_file_list1:
    with open(item1, 'r') as f:
        file1 += f.readlines()

#-----iterate through concatenated list of lines, extract protein sequences, output into file
with open(f'{output_filename1}.fasta', 'w') as g:
    seq_name1 = ''
    seq_start1 = False
    contig_name1 = ''
    seq1 = ''
    protein_start1 = False
    temp_fasta_header1 = ''
    name_seq_dict1 = {}

    for line1 in file1:
        #-----start recording when gene is defined
        if '# start gene' in line1:
            line2 = line1.replace('# start gene ', '').replace('\n', '')
            seq_name1 = line2
            seq_start1 = True
        #-----identify contig or scaffold to attach to associate with coding sequence
        elif ('contig_' in line1) or ('scaffold_' in line1):
            contig_name1 = line1.split('\t')[0]
        #-----identify beginning of protein sequence
        elif ('# protein sequence' in line1):
            line2 = line1.split('[')[1].replace('\n', '')
            protein_start1 = True
            #-----in some cases protein sequence starts and finishes in the same line; this accounts for that
            if ']' in line2:
                line2 = line2.split(']')[0]
                protein_start1 = False
                temp_fasta_header1 = '>' + str(contig_name1) + '_' + str(seq_name1) + '\n'
                seq1 += line2 + '\n'
                g.write(temp_fasta_header1)
                g.write(seq1)
                seq1 = ''
                contig_name1 = ''
                #seq_name1 = ''
            #-----when protein sequence spans >1 line, this starts reading sequences in the new line
            else:
                seq1 += line2
        #-----identify middle of protein sequences that span >1 line
        elif (protein_start1 == True) & (']' not in line1):
            seq1 += line1.replace('# ', '').replace('\n', '')
        #-----identify end of protein sequences that span >1 line
        elif (protein_start1 == True) & (']' in line1):
            seq1 += line1.split(']')[0].replace('# ', '') + '\n'
            temp_fasta_header1 = '>' + str(contig_name1) + '_' + str(seq_name1) + '\n'
            g.write(temp_fasta_header1)
            g.write(seq1)
            seq1 = ''
            contig_name1 = ''
            #seq_name1 = ''
            protein_start1 = False

#-----iterate through output file and assign unique number to each sequence (appended to end of fasta header for each entry) then output into new fasta
with open(f'{output_filename1}.fasta', 'r') as f:
    file1 = f.readlines()
    
with open(f'{output_filename1}.uniquenames.fasta', 'w') as g:
    temp_counter1 = 0
    for line1 in file1:
        if line1[0] == '>':
            line2 = line1.replace('\n', '')
            line3 = line2 + f'_{unique_name1}_' + str(temp_counter1) + '\n'
            g.write(line3)
            temp_counter1 += 1
        else:
            g.write(line1)
