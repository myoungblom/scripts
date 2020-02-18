#!/usr/bin/env python3

import sys

#####
# This script takes a snp-sites vcf and outputs a text file
# with the number of snps per isolate.
#####

# check for correct arguments
if len(sys.argv) != 2:
	print("Usage: vcfSnpCounts.py <snpsites.vcf>")
	sys.exit(0)

vcf = sys.argv[1]
outfile = vcf.split(".")[0]+"_SNPcounts.txt"
output = open(outfile, "w")
counts = {}
ids = []
with open(vcf, "r") as f:
	for line in f:
		line = line.strip("\n")
		if line.startswith("#CHROM"):
			ids = line.split("\t")
			for i in ids[9:]:
				ids.append(i)
				counts[ids.index(i)] = 0
		elif line.startswith("1"):
			snps = line.split("\t")
			counter = 9
			for i in snps[9:]:
				counts[counter] += int(i)
				counter += 1

for k in sorted(counts, key=counts.get, reverse=True):
	output.write(ids[int(k)]+"\t"+str(counts[k])+"\n")

output.close()
