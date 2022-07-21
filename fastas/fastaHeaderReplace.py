#!/usr/bin/env/ python

import sys
from Bio import SeqIO

#####
# This file takes in a fasta file, and a tab-delim file ("originalheader"\t"newheader) and 
# outputs a new fasta file with different headers.
#####

# check for correct commandline arguments
if len(sys.argv) != 3:
	print("Usage: searchAndReplace.py <fasta file> <headers to replace>")
	sys.exit(0) 

fastaFile = sys.argv[1]
headerFile = sys.argv[2]
outFile = fastaFile.strip(".fasta")+"_replaced.fasta"
headers = {}

with open(headerFile,"r") as f:
	for line in f:
		line = line.strip("\n")
		headers[line.split("\t")[0]] = line.split("\t")[1]

fasta = open(fastaFile,"r")
newHeaders = []
output = open(outFile,"w")
seqs = SeqIO.parse(fasta,"fasta")

for record in seqs:
	record.description = headers[record.id]
	record.id = headers[record.id]
	newHeaders.append(record)

SeqIO.write(newHeaders,output,"fasta")
fasta.close()
output.close()
