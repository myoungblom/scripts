#!/usr/bin/env python

import sys
import itertools
import os

#####
# This script uses a genome annotation file in bed format to
# append gene information to an Fst output file produced i
# by Vcflib (filtered and converted to csv in R).
#####

# check for correct arguments
if len(sys.argv) != 3:
	print("Usage: fstResultsToGenes.py <FstOutput.csv> <annotations.bed>")
	sys.exit(0)

fst = sys.argv[1]
temp = fst.split(".")[0]+".tmp"
tempOut = open(temp, "w")
outFile = fst.split(".")[0]+"_annotated.csv"
bed = sys.argv[2]

outliers = []
fstDict = {}
with open(fst, 'r') as f:
	header = next(f).strip("\n")
	tempOut.write(header+",geneStart,geneStop,Strand,Annotation\n")
	for line in f:
		tempOut.write(line)
		line = line.strip("\n")
		position = line.split(",")[2]
		outliers.append(position)
tempOut.close()

with open(bed, 'r') as annot:
	for line in annot:
		line = line.strip("\n")
		info = line.split("\t")
		start = int(info[1])
		stop = int(info[2])
		posList = list(range(start, stop+1))
		writeOut = ("%i,%i,%s,%s" % (start,stop, info[5], info[9]))
		for pos in posList:
			if str(pos) in outliers:
				fstDict[str(pos)] = writeOut

with open(outFile, "w") as out:
	with open(temp, 'r') as infile:
		out.write(next(infile))
		for line in infile:
			position = str(line.split(",")[2])
			if position in fstDict:
				annotation = fstDict[position]
				out.write(line.strip("\n")+","+annotation+"\n")
			else:
				out.write(line.strip("\n")+","+"intergenic"+"\n")
os.remove(temp)
