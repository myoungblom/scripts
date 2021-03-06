#!/usr/bin/env python

import sys
from Bio import SeqIO
import itertools
from collections import OrderedDict
import textwrap
import os

#######
# This file takes in mummer output from 'show-snps -T' and produces a fasta sequence
# using the reference sequence used to call the snps with nucmer.
# ** will ignore insertions **
# ** outputs single contig, named identically to 'outputfile' name given as argument **
#######

#######
# Correct usage of mummer for using this script is as follows:
# nucmer --maxmatch -p <prefix> <ref_seq> <query_seq> # its important the ref seq comes first for this command
# show-snps -T prefix.delta > prefix.snps # SNP-table output must be directed to a text file
#######

# check for correct arguments
if len(sys.argv) != 4:
	print("Usage: mummerToFasta.py <SNP file> <outputfile> <reference>")
	sys.exit(0)

InFileName = sys.argv[1] #SNP table from nucmer & show-snps
OutFileName = sys.argv[2] #Fasta format
TmpFile = OutFileName.split(".")[0] + ".tmp" #Temporary file
RefName = sys.argv[3] #Reference sequence

# verify reference sequence has only 1 contig
print("Reading reference sequence ...")
reference = SeqIO.parse(RefName, "fasta")
if len(list(reference)) > 1:
	print("Reference sequence must contain only 1 contig")
	sys.exit(0)

# parse mummer input file, make list of all SNPs & positions in reference
RefPos = [] # positions of SNPs in reference
SNPs = [] # SNPs

print("Parsing SNP table ...")
with open(InFileName, 'r') as InFile:
	for line in InFile:
		if (line.split('\t')[0]).isdigit(): # start parsing SNP table after headers
			wordlist = line.split('\t') # create list of values from each line
			if wordlist[1] != '.':	    # skip insertion sites
				RefPos.append(wordlist[0]) # make list of positions in reference with SNPs/deletions
				if wordlist[2] == '.':	   # change deletions to '-' for continuity with RGA
					SNPs.append('-')
				else:
					SNPs.append(wordlist[2]) # make list of SNPs

# create dictionary for each position:nt
print("Creating SNP dictionary ...")
SNP_dict = OrderedDict(itertools.izip(RefPos, SNPs))

# write reference sequence to temp file, to be edited according to SNP table
for ref_seq in SeqIO.parse(RefName, "fasta"):
        print("Writing reference sequence: "+ ref_seq.id + " to temporary file")
        ref_seq.id = OutFileName.split(".")[0] # change seq id to match filename
        ref_seq.description = OutFileName.split(".")[0]
        SeqIO.write(ref_seq, TmpFile, "fasta") # write ref seq to temp file
        print("New sequence identifier: " + ref_seq.id)

# edit reference sequence in temp file based on SNPs/gaps in mummer output, write to output file
print("Making SNPs in reference sequence ...")
OutFile = open(OutFileName, 'w')
with open(TmpFile, 'r') as temp_seq:
	sequence_to_edit = temp_seq.read()
	header, sequence = sequence_to_edit.split('\n', 1)
	sequence = sequence.replace('\n','') + '\n'
	sequence = list(sequence)
	for Pos, SNP in SNP_dict.iteritems():
		sequence[int(Pos) - 1] = str(SNP)
	sequence = "".join(sequence)
	print("Writing edited sequence to outfile ...")
	OutFile.write(header + '\n')
#	wrapped_seq = textwrap.fill(seq, width=60) # text wrapping in script wasn't working, will fix later
#	print(wrapped_seq[:100])
#	OutFile.write(wrapped_seq)
	OutFile.write(sequence)
		
OutFile.close()
os.remove(TmpFile)
print("Deleting temporary file ...")	
