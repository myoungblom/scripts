#!/usr/bin/env/ python

import sys
from Bio import SeqIO

#####
# This file takes in a fasta file, and a tab-delim file ("originalheader"\t"newheader) and 
# outputs a new fasta file with different headers.
#####

# check for correct commandline arguments
if len(sys.argv) != 2:
	print("Usage: contigLength.py <fasta file>")
	sys.exit(0) 

fastaFile = sys.argv[1]
fasta = open(fastaFile,"r")
seqs = SeqIO.parse(fasta,"fasta")

for record in seqs:
	print record.id,len(record.seq)

fasta.close()
