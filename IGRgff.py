#!/usr/bin/env python

import sys

#####
# This script takes a GFF and outputs a GFF with added intergenic regions.
#####

# check for correct arguments
if len(sys.argv) != 2:
	print("Usage: IGRgff.py <gff>")
	sys.exit(0)

gff = sys.argv[1]
out = gff.strip(".gff")+"_IGR.gff"
output = open(out, "w")
geneDict = {}

# get end of first coding region
with open(gff, "r") as f:
	for line in f:
		line = line.strip("\n")
		if not line.startswith("#"):
			parser = line.split("\t")
			feature = parser[2]
			end = parser[4]
			if feature == "gene":
				IGRstart = int(end)
				break

with open(gff, "r") as f:
	counter = 1
	for line in f:
		line = line.strip("\n")
		if not line.startswith("#"):
			parser = line.split("\t")
			feature = parser[2]
			start = parser[3]
			end = parser[4]
			if feature == "gene" and start != "1" and int(end)>int(start):
				IGRend = int(start)-1
				if IGRend > IGRstart:
					output.write("\t".join(parser[:2])+"\tIGR\t"+str(IGRstart)+"\t"+str(IGRend)+"\t.\t+\t.\tID=IGR"+str(counter)+";Name=IGR"+str(counter)+"_"+str(IGRstart)+"_"+str(IGRend)+"\n")
					IGRstart = int(end)+1
					counter += 1
		output.write(line+"\n")
