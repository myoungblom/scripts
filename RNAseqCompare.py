#!/usr/bin/env python

import sys

#####
# This script takes two (or more) lists of RNAseq results, a primary and a seconary list, then compares the secondary
# list to the primary list. The output is a csv file with the primary list, and a column of UP/DOWN regulation
# from the seconary list, or an empty space if the gene was not present in the seconary list.
#####

# check for correct command line arguments
if len(sys.argv) < 3:
	print("Usage: RNAseqCompare.py <primarylist.csv> <secondarylist.csv> ... ")
	sys.exit(0)

primaryFile = sys.argv[1]
secondaryFiles = sys.argv[2:]
outputFile = primaryFile.strip(".csv")+"_compare.csv"

reg = {}

with open(primaryFile, "r") as f:
	for line in f:
		line = line.strip()
		info = line.split(",")
		gene = info[0]
		reg[gene] = []

header = [primaryFile.strip(".csv")]
for f in secondaryFiles:
	tmpDict = {}
	header.append(f.strip(".csv"))
	with open(f, "r") as geneList:
		for line in geneList:
			line = line.strip()
			info = line.split(",")
			gene = info[0]
			direction = info[1]
			tmpDict[gene] = direction
	for gene in reg.keys():
		if gene in tmpDict.keys():
			reg[gene].append(tmpDict[gene])
		else:
			reg[gene].append("")


with open(outputFile, "w") as out:
	out.write(",".join(header)+"\n")
	for key,value in reg.items():
		out.write(key+","+",".join(value)+"\n")

	
