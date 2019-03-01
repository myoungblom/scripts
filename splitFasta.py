#!/usr/bin/env python

import sys
import os
from Bio import SeqIO

##########
# This script splits mutlifasta files into individual fasta files. Output files will be named
# for each fasta header.
##########

# check for correct arguments
if len(sys.argv) != 2:
	print("Usage: splitFasta.py <inputfile.fasta>")
	sys.exit(0)

input_file = sys.argv[1]

# list number of sequences
total_seq = list(SeqIO.parse(input_file, "fasta"))
print(str(len(total_seq)) + " sequences")


# make output file for each sequence
for sequence in total_seq:
	print(sequence.id)
	output = open(sequence.id+".fasta", "w")
	SeqIO.write(sequence, output, "fasta")
	output.close()


