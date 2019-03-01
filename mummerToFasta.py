#!/usr/bin/evn python

import sys
from Bio import SeqIO


#######
#This script takes in the output from mummer/nucmer 'show-snps -T' and creates a fasta alignment
#using the reference sequence used to call the snps with nucmer.
#
#######

# check for correct command line arguments
if len(sys.argv) != 4:
	print("Usage: mummerToFasta.py <input file> <outputfile> <reference>")
	sys.exit(0)


InFileName = sys.argv[1] #Mummer output (output from 'show-snps -T')
OutFileName = sys.argv[2] #Fasta format
RefName = sys.argv[3] #Reference sequence

InFile = open(InFileName, 'r') #read mummer file
RefFile = open(RefName, 'r') #read reference file
OutFile = open(OutFileName, 'w') #write output file

# read reference sequence
# edit reference sequence based on SNPs/gaps in mummer output
# ignore insertions compared to reference
# write new sequence in fasta format


