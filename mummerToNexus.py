#!/usr/bin/evn python

import sys
import re
import itertools

#######
#This script takes in the output from mummer/nucmer 'show-snps -T' and creates a nexus alignment
#using the reference sequence used to call the snps with nucmer.
#
#######

# check for correct command line arguments
if len(sys.argv) != 5:
	print("Usage: mummerToNexus.py <input file> <outputfile> <reference> <NorALL>")
	sys.exit(0)


InFileName = sys.argv[1] #mummer output (output from 'show-snps -T')
OutFileName = sys.argv[2] #Nexus format
RefName = sys.argv[3] #Reference sequence
#NorAll = sys.argv[4] #Remove all ambiguous bases or just N

InFile = open(InFileName, 'r') #read mummer file
OutFile = open(OutFileName, 'w') #write output file

# list of SNPs (position, SNP, sequence) in mummer file


# create dictionary for each name:sequence



