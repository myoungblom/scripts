#!/usr/bin/env python3

import sys


#####
# This script parses a gubbins gff file
# and outputs recombinant fragment lengths and the number of isolates
# that share each recombinant fragment
#####

if len(sys.argv) != 2:
	print("Usage: gubbinsFragments.py <gubbins_out.gff>")
	sys.exit(0)

gff = sys.argv[1]
lout = gff.split(".")[0]+"_fragmentLengths.txt"
pout = gff.split(".")[0]+"_sharedFragments.txt"


lengths = []
shared = []

with open(gff,"r") as f:
	for line in f:
		if not line.startswith("#"):
			info = line.strip().split("\t")
			start = int(info[3])
			end = int(info[4])
			lengths.append(end-start)
			taxa = info[8].split(";")[2].split("=")[1].strip('"').strip(" ").split(" ")
			shared.append(len(set(taxa)))

with open(lout,"w") as out:
	for x in lengths:
		out.write(str(x)+"\n")

with open(pout,"w") as out:
	for x in shared:
		out.write(str(x)+"\n")
