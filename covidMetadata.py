#!/usr/bin/env python

import sys
from Bio import SeqIO

#####
# Converts metadata file downloaded from GISAID to format to be used 
# with Nextstrain pipeline, renames fasta headers to be shorter and adds
# second copy of Wuhan/WH01/2019 for rooting purposes.
#####

# check for correct command line arguments
if len(sys.argv) != 3:
	print("Usage: covidMetadata.py gisaid_metadata.tsv gisaid_seq.fasta")
	sys.exit(0)

# input files
metadata = sys.argv[1]
fasta = sys.argv[2]

# output files
metaOut = metadata.strip(".tsv")+"_nextstrain.tsv"
metaOutput = open(metaOut,"w")
fastaOut = fasta.strip(".fasta")+"_nextstrain.fasta"

# write header in metadata output file
metaOutput.write("Name\tContinent\tCountry\tDate\n")

# dictionary for rewriting fasta headers
names = {}

# reformat metadata file, make shorter names for each virus
with open(metadata, "r") as f:
	for line in f:
		line = line.strip("\n")
		info = line.split("\t")
		name = ("/".join(info[1].split("/")[1:])).replace(" ","")
		cont = info[2].split("/")[0]
		count = info[2].split("/")[1]
		date = info[3]
		oldName = ("|".join([info[1],info[0],date])).replace(" ","")
		names[oldName] = name
		metaOutput.write("\t".join([name,cont,count,date])+"\n")

metaOutput.close()
newSeqs = []

# parse fasta file, make a list of records  with new names
with open(fasta, "r") as f:
	seqs = SeqIO.parse(fasta, "fasta")
	for record in seqs:
		record.description = names[record.id]
		record.id = names[record.id]
		newSeqs.append(record)
		if record.id == "Wuhan/WH01/2019":
			record.description = "Wuhan-Hu-1/2019"
			record.id = "Wuhan-Hu-1/2019"
			newSeqs.append(record)

# write out records with new names to output file
fastaOutput = open(fastaOut,"w")		
SeqIO.write(newSeqs, fastaOut, "fasta")
fastaOutput.close
