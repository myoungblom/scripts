#! /usr/bin/env python

import sys
from Bio import SeqIO

######
# Prints base at give sequence position in fasta file
######

# check for correct arguments
if len(sys.argv) != 3:
	print("Usage: printSeq.py <fasta file> <position>")
	sys.exit(0)

InFileName = sys.argv[1]
Position = int(sys.argv[2])

# print base at given position
for seq in SeqIO.parse(InFileName, "fasta"):
	print("Base "+str(Position)+": "+str(seq[int(Position) - 1]))
