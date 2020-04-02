#!/usr/bin/env python

import sys
from Bio import SeqIO

#####
# This script takes a multifasta file of nrdM sequences and outputs
# a text file with the nrdM allele phenotypes for each isolate.
#####

# check for correct arguments
if len(sys.argv) != 2:
	print("Usage nrdMtyping.py <inputfile.fasta>")
	sys.exit(0)

inFile = sys.argv[1]
outFileName = inFile.split(".")[0] + "_nrdMtype.txt"
outFile = open(outFileName, 'w')

# read sequences to find isolates with ancestral allele
for oralis_seq in SeqIO.parse(inFile, "fasta"):
	if oralis_seq.seq[234 - 1] == "C":
		outFile.write(oralis_seq.id + '\tC\n')
	elif oralis_seq.seq[234-1] == "T":
		outFile.write(oralis_seq.id + "\tT\n")

outFile.close()
