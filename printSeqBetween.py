#! /usr/bin/env python

import sys
from Bio import SeqIO

######
# Prints base at give sequence position in fasta file
######

# check for correct arguments
if len(sys.argv) != 4:
	print("Usage: printSeq.py <fasta file> <position1> <position2>")
	sys.exit(0)

InFileName = sys.argv[1]
pos1 = int(sys.argv[2])-1
pos2 = int(sys.argv[3])

# print base at given position
for seq in SeqIO.parse(InFileName, "fasta"):
	print(pos1,pos2)
	print(seq.seq[pos1:pos2])
