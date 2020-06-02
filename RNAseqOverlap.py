#!/usr/bin/env python

import sys
import numpy as np


#####
# This script takes a list of all genes, the length (x) of a list to sample, and the list you're comparing to. 
# Genes are randomly sampled in size x from all genes, and compared to the final list to assess significant overlap
# (for RNAseq results being compared to published datasets).
#####

# check for correct command line arguments:
if len(sys.argv) != 4:
	print("Usage: RNAseqOverlap.py <allGenes.txt> <length> <comparisonList.txt>")
	sys.exit(0)

allGenesFile = sys.argv[1]
length = int(sys.argv[2])
comparisonFile = sys.argv[3]

allGenes = []
comparisonGenes = []

# read file of all genes into a list
with open(allGenesFile, "r") as f:
	for line in f:
		line = line.strip()
		allGenes.append(line)

# read file of comparison genes into a list
with open(comparisonFile, "r") as f:
	for line in f:
		line = line.strip()
		comparisonGenes.append(line)

# sample from all genes 100 times, making list of number of overlaps
allOverlaps = []
for i in range(100):
	subsetOverlap = 0
	subset = list(np.random.choice(allGenes, size=length, replace=False))
	for x in subset:
		if x in comparisonGenes:
			subsetOverlap += 1
	allOverlaps.append(subsetOverlap)

print("Min. overlap: "+ str(min(allOverlaps)))
print("Mean overlap: "+ str(np.average(allOverlaps)))
print("Max. overlap: "+ str(max(allOverlaps)))
