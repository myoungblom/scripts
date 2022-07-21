#!/usr/bin/env python

import sys
from Bio import SeqIO

#####
#
#####

if len(sys.argv) < 2:
	print("Usage: script.py fasta.fasta")
	sys.exit(0)

fastas = sys.argv[1:]

for fasta in fastas:
	isolate = fasta.split("_")[0]
	outfile = fasta.split(".")[0]+"_renamed.fasta"
	num = 1
	renamed_contigs = []
	for contig in SeqIO.parse(fasta,"fasta"):
		contig.id = isolate+"_"+str(num)
		contig.description = isolate+"_"+str(num)
		renamed_contigs.append(contig)
		num += 1
	with open(outfile,"w") as out:
		SeqIO.write(renamed_contigs,out,"fasta")
