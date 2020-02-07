#!/usr/bin/env python

import sys
import glob
import os


#####
# This script takes a directory with fastq files from multiple lanes and a text file containing isolate ID's
# and concatenates/renames them into a single forward and reverse read for each isolate.
#####

if len(sys.argv) != 3:
	print("Usage: concatenateReads.py <fastq-dir> <ids.txt>")
	sys.exit(0)

fq_dir = sys.argv[1]
id_file = sys.argv[2]
files = {}
ids = []
with open(id_file, "r") as f:
	for line in f:
		line = line.strip("\n")
		ids.append(line)
		files[line+"_1.fastq.gz"] = []
		files[line+"_2.fastq.gz"] = []

for i in glob.glob(fq_dir+"/*fastq*"):
	newname = i.split("-")[0]
	newname = newname.strip("./")
	if "R1" in i:
		files[newname+"_1.fastq.gz"].append(i)
	elif "R2" in i:
		files[newname+"_2.fastq.gz"].append(i)

for i,j in files.items():
	for f in j:
		os.system("cat "+f+" >> "+i)
