#!/usr/bin/env python

import sys

#####
# This script takes in a Roary gene presence absence csv file
# and a text file containing genes of interest and outputs a
# subset presence absence file for use with plotting in R.
#####


# check for correct arguments
if len(sys.argv) != 3:
	print("Usage: gpaGeneMatrix.py <roary_GPA.csv> <genes.txt>")
	sys.exit(0)

gpa = sys.argv[1]
output = gpa.strip(".csv")+"_GeneMatrix.csv"
txt = sys.argv[2]

# make list of genes of interest
genes = []
with open(txt, "r") as f:
	for line in f:
		line = line.strip("\n")
		genes.append(line)

# read csv, write out presence/absence file
out = open(output, 'w')
gene_dict = {}
with open(gpa, 'r') as f:
	isolates = next(f).split(",")[14:]
	for iso in isolates:
		gene_dict[iso] = []
	for line in f:
		line = line.strip("\n")
		info = line.split(",")
		gene = info[0].strip("\"")
		if gene in genes:
			counter = 14
			for x in info[14:]:
				x = x.strip("\"")
				index = isolates[counter-14]
				if x == "":
					gene_dict[index].append("absent")
				else:
					gene_dict[index].append("present")
				counter += 1

out.write("isolate,"+",".join(genes)+"\n")
for key,value in gene_dict.items():
	out.write(key.strip("_annot")+",")
	out.write(",".join(value)+"\n")

out.close()
