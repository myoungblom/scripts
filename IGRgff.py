#!/usr/bin/env python

import sys
import os
import subprocess

#####
# This script takes a GFF and a text file with chromosome sizes,
# and outputs a GFF with added intergenic regions.
#
# Chromosome size file format:
# chrom_name\tchrom_size
#####

# check for correct arguments
if len(sys.argv) != 3:
	print("Usage: IGRgff.py <gff> <chrom_sizes>")
	sys.exit(0)

gff = sys.argv[1]
chrom = sys.argv[2]
IGRout = gff.strip(".gff")+"_IGR.gff"

# format gff for bedtools
sortedGff = gff.strip(".gff")+"_sorted.gff"
sortedGenesGff = sortedGff.strip(".gff")+"_genes.gff"
IGR = gff.strip(".gff")+"_IGR.tmp"
output = open(IGR,"w")
# sorting gff by position
command = "cat "+gff+''' | awk '$1 ~ /^#/ {print $0;next} {print $0 | "sort -k1,1 -k4,4n -k5,5n"}' >'''+sortedGff
subprocess.call(command,shell=True)
# removing all 'CDS' and 'region' gff entries
command = "grep -v CDS "+sortedGff+" | grep -Pv '\tregion\t' > "+sortedGenesGff
subprocess.call(command,shell=True)
# using bedtools complement to get coordinates of intergenic regions
subprocess.call(["bedtools","complement","-i", sortedGenesGff,"-g",chrom],stdout=output)
output.close()

# read IGR coordinates into dictionary
gffDict = {}
counter = 1
with open(IGR,"r") as f:
	for line in f:
		line = line.strip("\n")
		info = line.split("\t")
		start = info[1]
		end = info[2]
		if not (start == "0" and end == "0"):
			name = "Name=IGR"+str(counter)+"_"+start+"_"+end
			line = "gene\t"+start+"\t"+end+"\t"+".\t+\t.\t"+name
			gffDict[int(start)] = line
			counter += 1

# read gff coordinates into dictionary
with open(sortedGenesGff, "r") as f:
	for line in f:
		if not line.startswith("#"):	
			line = line.strip("\n")
			info = line.split("\t")
			start = info[3]
			header = info[:2]
			gffDict[int(start)] = "\t".join(info[2:])

# sort dictionary by start position
keys = [x for x in gffDict.keys()]
sorted_keys = sorted(keys)

# write gff with IGRs to output by start coordinate
header = "\t".join(header)
with open(IGRout, "w") as out:
	for pos in sorted_keys:
		out.write(header+"\t"+gffDict[pos]+"\n")

os.remove(sortedGff)
os.remove(sortedGenesGff)
os.remove(IGR)
