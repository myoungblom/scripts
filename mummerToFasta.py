#!/usr/bin/evn python

import sys
from Bio import SeqIO
import itertools
from collections import OrderedDict
from Bio.Seq import MutableSeq

#######
# This file takes in mummer output from 'show-snps -T' and produces a fasta sequence
# using the reference sequence used to call the snps with nucmer.
# ** will ignore insertions **
# ** outputs single contig, named identically to 'outputfile' name given as argument **
#######

#######
# Correct usage of mummer for using this script is as follows:
# nucmer --prefix=whatever <ref_seq> <query_seq> # its important the ref seq comes first for this command
# show-snps -T whatever.delta > whatever.snps # SNP-table output must be directed to a text file
#######

# check for correct arguments
if len(sys.argv) != 4:
	print("Usage: mummerToFasta.py <SNP file> <outputfile> <reference>")
	sys.exit(0)

InFileName = sys.argv[1] #SNP table from nucmer & show-snps
OutFileName = sys.argv[2] #Fasta format
RefName = sys.argv[3] #Reference sequence

OutFile = open(OutFileName, 'w') #write output file

# verify reference sequence has only 1 contig
print("Reading reference sequence ...")
seq = SeqIO.parse(RefName, "fasta")
if len(list(seq)) > 1:
	print("Reference sequence must contain only 1 contig")
	sys.exit(0)

# write reference sequence to outfile, to be edited according to SNP table
for ref_seq in SeqIO.parse(RefName, "fasta"):
	print("Writing reference sequence: "+ ref_seq.id + " to output file")	
	ref_seq.id = OutFileName.split(".")[0]
	ref_seq.description = OutFileName.split(".")[0]
	SeqIO.write(ref_seq, OutFile, "fasta")
	print("New sequence identifier: " + ref_seq.id)

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

# edit reference sequence based on SNPs/gaps in mummer output
for edit_seq in SeqIO.parse(OutFile, "fasta"):
	edit_seq = MutableSeq(edit_seq) 
for pos, snp in SNP_dict.iteritems():
	print(pos)
	print(snp)
	edit_seq[pos-1] = snp




