#!/usr/bin/env python

import sys
import os
from Bio import SeqIO

#######
# This script takes a fasta file, and sequence ID's (or a text file with ID's) and
# pulls those sequences out into individual fasta files.
# ** must be no spaces in sequence headers!! (:%s/ \//g to remove spaces) **
#######

# check for correct commandline arguments
if len(sys.argv) <= 2:
	print("Usage: pullFromFasta.py <fasta file> <ids/txt file to remove>")
	sys.exit(0)

# check if id's to pull are in text file or as arguments
is_file = os.path.isfile('./'+sys.argv[2])

# parse sequence id's to pull
seq_to_pull = []

if is_file:
	print("Id's from text file will be pulled from fasta file:")
	with open(sys.argv[2], 'r') as txtfile:
		for i, line in enumerate(txtfile):
			line = line.strip().split('\t')
			seqID = line[0]
			seq_to_pull.append(seqID)
			print(seqID)

else:
	print("Id's given as arguments will be pulled from fasta file:")
	for ID in sys.argv[2:]:
		seq_to_pull.append(ID)
		print(ID)

# parse fasta file, write pulled sequences to new fasta files
for seq in SeqIO.parse(sys.argv[1], "fasta"):
	if seq.id in seq_to_pull:
		output = open((seq.id).replace("/","")+".fasta", "w")
		SeqIO.write(seq, output, "fasta")
		output.close()
