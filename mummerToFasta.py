#!/usr/bin/evn python

import sys
from Bio import SeqIO
import itertools

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

InFile = open(InFileName, 'r') #read mummer file
RefFile = open(RefName, 'r') #read reference file
OutFile = open(OutFileName, 'w') #write output file

# check that correct reference has been provided &
# that reference sequence only has 1 contig
sequence = SeqIO.parse(RefFile, "fasta")
if len(list(sequence)) != 1:
        print("Reference sequence must contain only 1 contig")
        sys.exit(0)


# parse mummer input file, make list of all SNPs & positions in reference
RefPos = [] # positions of SNPs in reference
SNPs = [] # SNPs

print("Parsing SNP table ...")

for line in InFile:
	if (line.split('\t')[0]).isdigit(): # start parsing SNP table after headers
		wordlist = line.split('\t') # create list of values from each line
		if wordlist[1] != '.':	    # skip insertion sites
			RefPos.append(wordlist[0]) # make list of positions in reference with SNPs/deletions
			if wordlist[2] == '.':	   # change deletions to '-' for continuity with RGA
				SNPs.append('-')
			else:
				SNPs.append(wordlist[2]) # make list of SNPs
print(RefPos[:4])
print(SNPs[:4])

# create dictionary for each position:nt
print("Creating SNP dictionary ...")
SNP_dict = dict(itertools.izip(RefPos, SNPs))

# write reference sequence to ouput file, to be edited
print("Writing sequence to outfile ...")
OutFile.write('>' + OutFileName.split(".")[0] + '\n')
print("	Writing output header ...")

for ref_seq in SeqIO.parse(RefName, "fasta"):
	OutFile.write(ref_seq)
print("		Writing reference seq to outfile ...")






#	OutFile.write(sequence)
	
#	if len(sequence) != 1:
#	else:
#		SeqIO.write(sequence, OUtFile, "fasta")
#		output.close()


# parse mummer input file



# read reference sequence
# write entire reference sequence to output file?
# 	or write reference as you go until you hit position in column1?
# for row in columns
#	if column2 == '.' skip
#	change position column1 to column3 in reference
#		if letter change to letter
#		if '.' change to '-'
# edit reference sequence based on SNPs/gaps in mummer output
# ignore insertions compared to reference
# write new sequence in fasta format
