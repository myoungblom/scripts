#!/usr/bin/env python3

import sys
import os.path
from Bio import Phylo

#####
# This script takes a snp-sites vcf, a tree in newick format, and a list or file containing snps of interest
# (given as positions in alignment),and outputs a csv file with presence absence values to be used for plotting matrix in R.
#####

# check for correct arguments
if len(sys.argv) < 4:
	print("Usage: vcfSnpCounts.py <snpsites.vcf> <tree.newick> <list/textfile>")
	sys.exit(0)

# check if snps are given as argument or as text file
is_file = os.path.isfile("./"+sys.argv[3])
snps = []
if is_file:
	with open(sys.argv[3], "r") as txt:
		for line in txt:
			snps.append(int(line.strip()))
else:
	for i in sys.argv[3:]:
		snps.append(i)


vcf = sys.argv[1]
outfile = vcf+"_SNPmatrix.csv"
output = open(outfile, "w")
iso = {}
names = []
tree = Phylo.read(sys.argv[2],"newick")
term = tree.get_terminals()

with open(vcf, "r") as f:
	for line in f:
		line = line.strip("\n")
		if line.startswith("#CHROM"):
			ids = line.split("\t")
			for i in ids[9:]:
				names.append(i)
				iso[i] = []
		elif line.startswith("1"):
			info = line.split("\t")
			if int(info[1]) in snps:
				output.write(","+info[3]+info[1]+info[4])
				counter = 9
				for i in info[9:]:
					iso[names[counter-9]].append(i)
					counter += 1
output.write("\n")
for key,value in iso.items():
	output.write(key+",")
	output.write(",".join(value)+"\n")

output.close()
