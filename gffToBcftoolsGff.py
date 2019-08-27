#!/usr/bin/env python

import sys
import os
import subprocess

######
# This script takes a GFF file from roaryToCoreGFF.py and converts it
# to a GFF that is compatible with bcftools-csq for consequence annotation.
######

# check for correct arguments
if len(sys.argv) != 2:
    print("Usage: roaryToBcftoolsGFF.py <gff file>")
    sys.exit(0)

gff = sys.argv[1] 
outfile = gff.split(".")[0]+"_bcftools.gff"
output = open(outfile, "w")

with open(gff, "r") as f:
    for line in f:
        if line.startswith("#"):
            output.write(line)
        elif not line.startswith("#"):
            line = line.strip("\n")
            gene = (line.replace("misc_feature", "gene")).replace("feature", "gene")
            firstpos = gene.split("\t")[8].split(";")[0]
            if firstpos.startswith("ID"):
                ID1 = firstpos
                ID2 = ID1.replace("ID=","ID=gene:")
            elif firstpos.startswith("label="):
                ID1 = firstpos
                ID2 = ID1.replace("label=", "ID=gene:")
            else:
                ID1 = gene.split("\t")[8].split(";")[1]
                ID2 = ID1.replace("ID=", "ID=gene:")
            gene = gene.replace(ID1, ID2)
            transcriptID = ID2.replace("ID", "Parent")
            transcript = (gene.replace("ID=gene:", "ID=transcript:")).replace("gene", "transcript")
            transcript = transcript+";"+transcriptID
            cds = transcript.replace("ID=transcript:", "ID=CDS:").replace("Parent=gene:", "Parent=transcript:").replace("\ttranscript", "\tCDS")
            output.write(gene+";biotype=protein_coding\n")
            output.write(transcript+";biotype=protein_coding\n")
            output.write(cds+"\n")
output.close()

