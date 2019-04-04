#!/usr/bin/env python

import sys
from Bio import SeqIO

#####
# This script returns a text file with the sequence IDs of all Staphylococcus saprophyticus 
# isolates which have the ancestral AAS allele ("A" at position 1,811,777 in RGA)
#####

# check for correct arguments
if len(sys.argv) != 2:
	print("Usage aasTyping.py <inputfile.fasta>")
	sys.exit(0)

inFile = sys.argv[1]
outFileName = inFile.split(".")[0] + "_ancAAS.txt"
outFile = open(outFileName, 'w')

# read sequences to find isolates with ancestral allele
for sapro_seq in SeqIO.parse(inFile, "fasta"):
	if sapro_seq.seq[1811777 - 1] == "A":
		outFile.write(sapro_seq.id + '\n')

outFile.close()
