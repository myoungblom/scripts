#!/usr/bin/env/ python

import sys
from Bio import SeqIO

#####
# This script takes in an assembly from SPAdes and filters out
# contigs which are shorter than 500bp and/or lower than 5X coverage.
#####


# check for correct commandline arguments
if len(sys.argv) != 2:
    print("Usage: contigFilter.py <contigs.fasta>")
    sys.exit(0)

inFile = sys.argv[1]
outFile = inFile.split(".")[0]+"_filtered.fasta"


# filter out contigs that are <500bp and/or <5X coverage
output = open(outFile, 'w')
quality_contigs = []

for contig in SeqIO.parse(inFile, "fasta"):
    coverage = float((contig.id).split("_")[-1])
    length = len(contig.seq)
    if length > 500 and coverage > 5.0:
            quality_contigs.append(contig)

SeqIO.write(quality_contigs, outFile, "fasta")
output.close()
