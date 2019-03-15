#!/usr/bin/env python

import sys
import os
from Bio import SeqIO

####
#This scripts returns the lenth of each contig in a fasta file
####

# check for correct arguments
if len(sys.argv) != 3:
	print("Usage: contigLength.py <inputfile.fasta> <outputfile>")
	sys.exit(0)

input_file = sys.argv[1]
output_file = sys.argv[2]

output = open(output_file + ".txt", 'w')


# total number of contigs
total_contigs = list(SeqIO.parse(input_file, "fasta"))
output.write(input_file + ":" + str( len(total_contigs)) + " contigs\n")

# length of each contig & average length
total_length = 0

for contig in SeqIO.parse(input_file, "fasta"):
	output.write(contig.id +"\n")
	output.write(str(len(contig)) + " bp" + "\n")
	total_length += len(contig)

average_length = total_length / len(total_contigs)
output.write("Total length:" + str(total_length) + " bp" + "\n")
output.write("Average contig length:" + str(average_length) + " bp" + "\n")

output.close()

