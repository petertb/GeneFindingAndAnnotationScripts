#!/bin/bash

#These scripts were adapted from "Predicting Genes in Single Genomes with Augustus"
#a manual written by Katharina J. Hoff and Mario Stanke that can be found here:
#https://currentprotocols.onlinelibrary.wiley.com/doi/full/10.1002/cpbi.57

#-----Notes:
# [1] 	These scripts were used to find coding genes in tick genome assemblies created
#		using PacBio CCS HiFi long-reads. Transcript-based hints were generated using 
#		the PacBio HiFi isoseq long-read method.
# [2]	This work was performed using Augustus 3.3.3 and Gmap version 2020-10-14
# [3]	These scripts were tested on a workstation-grade desktop equipped with a
#		10-core 3.7GHz Xeon with 224Gb of RAM running Ubuntu 20.04.3 supported
#		by windows subsystem for linux

#-----Pre-run:
#create a new directory for this task and add (1) genome assembly, (2)isoseq fasta file, (3) this script,
#(4) augustus extrinsic configuration file, (5) 2x accessory python files for split and reassemble
#change directory into new location and once inside make this script executable "chmod +x script_name"

#-----Run:
#variables
ORGANISM_NAME1="amblyommaamericanum"
ASSEMBLY_NAME1="02_T1T2_flye_assembly_purged.fasta"
ISOSEQ_NAME1="subreads_ccs.flnc.polished.hq.hq.fasta"
NUMBER_OF_THREADS1=20

#create new subdirectory for gmap index
mkdir gindex
#build gmap index
gmap_build -D gindex/ -d $ORGANISM_NAME1 $ASSEMBLY_NAME1
gmap -D gindex/ -d $ORGANISM_NAME1 $ISOSEQ_NAME1 --min-intronlength=30 --intronlength=500000 --trim-end-exons=20 -f 1 -n 0 -t $((NUMBER_OF_THREADS1-2)) -O > gmap.psl
#create hints file
cat gmap.psl | sort -n -k 16,16 | sort -s -k 14,14 | perl -ne '@f=split; print if ($f[0]>=100)' | blat2hints.pl --source=PB --nomult --ep_cutoff=20 --in=/dev/stdin --out=isoseq.gff

#create new subdirectory
#split genome into smaller pieces for parallelization (number of splits is 2 less than number of cores defined in variables)
mkdir Augustus_split
python3 combined_script1_accessory1.py $ASSEMBLY_NAME1 $NUMBER_OF_THREADS1 ./Augustus_split/

#run augustus on each genome split, output files into new folder
mkdir Augustus_output
for i in ./Augustus_split/*.fasta; do
	augustus --species=fly --extrinsicCfgFile=./extrinsic.M.RM.PB.cfg --hintsfile=isoseq.gff --allow_hinted_splicesites=atac $i > ./Augustus_output/${i//"./Augustus_split/"}.out &
done

#-----Post-run:
#collect protein sequences from each Augustus output file and concatenate into new fasta file
#give each fasta document a unique identifier for downstream processing
FILE_LIST1=(Augustus_output/*.out)
python3 combined_script1_accessory2.py $ORGANISM_NAME1 ${FILE_LIST1[@]} 