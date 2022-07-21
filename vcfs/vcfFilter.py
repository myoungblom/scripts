#!/usr/bin/env python

import sys

#####
# This script takes in a set of vcf files output by pilon, and a bed file of regions to 
# filter out from pilon results.
#####

if len(sys.argv) < 3:
	print("Usage: breseqFilter.py <bed file> <vcf #1> ... <vcf #n>")
	sys.exit(0)


bed = sys.argv[1]
vcfs = sys.argv[2:]

def vcfFilter(vcf, bedCoor):
	with open(vcf, "r") as IN:
		with open(vcf.split(".")[0]+"_filtered.txt", "w") as OUT:
			for line in IN:
				if "#" not in line:
					line = line.strip()
					info = line.split("\t")
					pos = info[1]
					if int(pos) in bedCoor:
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

for vcf in vcfs:
	vcfFilter(vcf, bad_coordinates)
