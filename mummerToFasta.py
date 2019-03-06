#!/usr/bin/evn python

import sys
from Bio import SeqIO


#######
# This file takes in mummer output from 'show-snps -T' and produces a fasta sequence
# using the reference sequence used to call the snps with nucmer.
# ** will ignore insertions **
# ** outputs single contig, named identically to 'outputfile' name given as argument **
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
# write entire reference sequence to output file?
# 	or write reference as you go until you hit position in column1?
# for row in columns
#	if column2 == '.' skip
#	else
#	change position column1 to column3 in reference
#		if letter change to letter
#		if '.' change to '-'
# edit reference sequence based on SNPs/gaps in mummer output
# ignore insertions compared to reference
# write new sequence in fasta format


