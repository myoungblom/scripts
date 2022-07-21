#!/usr/bin/env python

import sys
import os.path
from Bio import SeqIO

###############
# This script removes seqences from a FASTA alignment
# takes id's to remove as arguments or a text file containing id's to remove
# ** headers must not contain spaces (:%s/\ //g to remove spaces)**
##################


# check for correct arguments
if len(sys.argv) <= 3:
	print("Usage: removeFromFasta.py <fasta file> <output fasta>  <ids/txt file to remove>")
	sys.exit(0)

# check if id's to remove are in text file or as arguments
is_file = os.path.isfile('./'+sys.argv[3])

# parse sequence id's to be removed
seq_to_remove = []

if is_file:
	print("Id's from text file will be removed from fasta file:")
	with open(sys.argv[3], 'r') as txtfile:
		for i, line in enumerate(txtfile):
			line = line.strip().split('\t')
			seqID = line[0]
			seq_to_remove.append(seqID) 
else:
	print("Id's given as arguments will be removed from fasta file:")
	for i in sys.argv[3:]:
		seq_to_remove.append(i)


# parse fasta file, write to new fasta file with only desired sequences
outfile = open(sys.argv[2]+".fasta", "w")
keep_sequences = []

for seq_record in SeqIO.parse(sys.argv[1], "fasta"):
	if seq_record.id in seq_to_remove:
		print("removed " + seq_record.id)
	else:
		keep_sequences.append(seq_record)

SeqIO.write(keep_sequences, outfile, "fasta")
outfile.close()
