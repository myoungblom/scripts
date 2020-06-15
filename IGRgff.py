#!/usr/bin/env python

import sys
import os
import subprocess
import shutil

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
# sortedGff: original gff file sorted by position
# sortedGenesGff: original gff file sorted, with "CDS" entries removed for use with bedtools
# IGRtmp: output of bedtools complement command
sortedGff = gff.strip(".gff")+"_sorted.gff"
sortedGenesGff = sortedGff.strip(".gff")+"_genes.gff"
IGRtmp = gff.strip(".gff")+"_IGR.tmp"
output = open(IGRtmp,"w")
# sorting gff by position
command = "cat "+gff+''' | awk '$1 ~ /^#/ {print $0;next} {print $0 | "sort -k1,1 -k4,4n -k5,5n"}' >'''+sortedGff
subprocess.call(command,shell=True)
# removing all 'CDS' and 'region' gff entries
command = "grep -v CDS "+sortedGff+" | grep -Pv '\tregion\t' > "+sortedGenesGff
subprocess.call(command,shell=True)
# using bedtools complement to get coordinates of intergenic regions
subprocess.call(["bedtools","complement","-i", sortedGenesGff,"-g",chrom],stdout=output)
output.close()

# read IGR coordinates into list
gffList = []
counter = 1
with open(IGRtmp,"r") as f:
	for line in f:
		line = line.strip("\n")
		info = line.split("\t")
		start = info[1]
		end = info[2]
		if not (start == "0" and end == "0"):
			name = "Name=IGR"+str(counter)+"_"+start+"_"+end
			line = "gene\t"+start+"\t"+end+"\t"+".\t+\t.\t"+name
			gffList.append(line)
			counter += 1

# get sequence ID and source from original gff file
with open(gff, "r") as f:
	for line in f:
		if not line.startswith("#"):	
			line = line.strip("\n")
			info = line.split("\t")
			header = info[:2]
			break

# copy contents of original gff to temporary IGR-gff output
IGRunsorted = "IGR_unsorted.tmp"
shutil.copyfile(gff,IGRunsorted)


# append IGR gff entries to original gff
header = "\t".join(header)
with open(IGRunsorted, "a") as out:
	for entry in gffList:
		out.write(header+"\t"+entry+"\n")

# sort output by position: original gff + IGR entries
command = "cat "+IGRunsorted+''' | awk '$1 ~ /^#/ {print $0;next} {print $0 | "sort -k1,1 -k4,4n -k5,5n"}' >'''+IGRout
subprocess.call(command,shell=True)

os.remove(sortedGff)
os.remove(sortedGenesGff)
os.remove(IGRtmp)
os.remove(IGRunsorted)
