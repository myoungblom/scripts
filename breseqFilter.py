#!/usr/bin/env python

import sys

#####
# This script takes in a set of gd files output by breseq, and a bed file of regions to 
# filter out from breseq results.
#####

if len(sys.argv) < 3:
	print("Usage: breseqFilter.py <bed file> <gd #1> ... <gd #n>")
	sys.exit(0)


bed = sys.argv[1]
gds = sys.argv[2:]

def gdFilter(gd, bedCoor):
	with open(gd, "r") as IN:
		with open(gd.split(".")[0]+"_filtered.gd", "w") as OUT:
			for line in IN:
				if line.startswith("#"):
					OUT.write(line)
				else:
					line = line.strip()
					info = line.split("\t")
					pos = info[4]
					if pos in bedCoor:
						print("Removed position "+pos)
					else:
						OUT.write(line+"\n")

def getBedCoor(bedfile):
	bedCoor = []
	with open(bedfile, "r") as f:
		for line in f:
			line = line.strip()
			info = line.split("\t")
			for i in range(int(info[1]), int(info[2])+1):
				bedCoor.append(i)
	return(bedCoor)

bad_coordinates = getBedCoor(bed)

for gd in gds:
	gdFilter(gd, bad_coordinates)
