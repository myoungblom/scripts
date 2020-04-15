#!/usr/bin/env python

import shutil
import sys
from Bio import SeqIO

#####
# Reformats metadata and sequence files for use with modified Nextstrain-ncov pipeline.
# Takes in: gisaid acknowledgements table (tsv), sequences in fasta format from gisaid.
# Output: updated metadata file for use with nextstrain pipeline, metadata for use with tree coloring, 
# reformatted fasta file.
#####

# check for correct command line arguments
if len(sys.argv) != 3:
	print("Usage: covidMetadata.py gisaid_metadata.tsv gisaid_seq.fasta")
	sys.exit(0)

# input files
metadata = sys.argv[1]
fasta = sys.argv[2]

# output files
treeOut = metadata.strip(".tsv")+"_tree.tsv"
treeOutput = open(treeOut,"w")
metaOut = metadata.strip(".tsv")+"_nextstrain.tsv"
metaOutput = open(metaOut,"w")
fastaOut = fasta.strip(".fasta")+"_nextstrain.fasta"
replace = open("replace_headers.txt","w")

# get genome lengths from fasta file
genome_lengths = {}
with open(fasta, "r") as f:
	seqs = SeqIO.parse(fasta, "fasta")
	for record in seqs:
		genome_lengths[record.id] = len(record.seq)

# write headers in metadata output files
treeOutput.write("Name\tContinent\tCountry\tDate\n")
metaOutput.write("strain\tvirus\tgisaid_epi_isl\tgenbank_accession\tdate\tregion\tcountry\
		\tdivision\tlocation\tregion_exposure\tcountry_exposure\tdivision_exposure\
		\tsegment\tlength\thost\tage\tsex\toriginating_lab\tsubmitting_lab\tauthors\
		\turl\ttitle\date_submitted\n")

# dictionary for rewriting fasta headers
names = {}

# reformat metadata file, make shorter names for each virus
uniqueIDs = []
with open(metadata, encoding="utf8", errors="ignore") as f:
	for line in f:
		line = line.strip("\n")
		info = line.split("\t")
		date = info[3]
		oldFastaHeader = ("|".join([info[1],info[0],date])).replace(" ","")
		newFastaHeader = ("/".join(info[1].split("/")[1:])).replace(" ","")
		nameWDate = ("/".join(info[1].split("/")[1:3])).replace(" ","")+"/"+date
		accession = info[0]
		region = (info[2].split("/")[0]).strip(" ")
		country = (info[2].split("/")[1]).strip(" ")
		try:
			division = (info[2].split("/")[2]).strip(" ")
		except IndexError:
			division = ""
		originating_lab = info[4]
		submitting_lab = info[5]
		authors = info[6]
		date_submitted = "?"	
		names[oldFastaHeader] = newFastaHeader
		if (oldFastaHeader in genome_lengths.keys()) and (newFastaHeader not in uniqueIDs):
			treeOutput.write(newFastaHeader+"\t"+region.replace(" ","")+"\t"+country.replace(" ","")+"\t"+date+"\n")
			replace.write(newFastaHeader+"\t"+nameWDate+"\n")
			length = genome_lengths[oldFastaHeader]
			line = "\t".join([newFastaHeader,"ncov",accession,"?",date,region,\
			country,division,"",region,country,division,"genome",str(length),\
			"Human","?","?",originating_lab,submitting_lab,authors,"https://www.gisaid.org",\
			"?",date_submitted])
			metaOutput.write(line+"\n")
			uniqueIDs.append(newFastaHeader)

metaOutput.close()
replace.close()
treeOutput.close()

newSeqs = []
uniqueSeqs = []

# parse fasta file, make a list of records  with new names
with open(fasta, "r") as f:
	seqs = SeqIO.parse(fasta, "fasta")
	for record in seqs:
		record.description = names[record.id]
		record.id = names[record.id]
		if record.id not in uniqueSeqs:
			newSeqs.append(record)
			uniqueSeqs.append(record.id)

# write out records with new names to output file
fastaOutput = open(fastaOut,"w")		
SeqIO.write(newSeqs, fastaOut, "fasta")
fastaOutput.close
