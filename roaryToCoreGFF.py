#!/usr/bin/env python

import sys
import os
import subprocess

######
# This file takes a core alignment header embl file (from Roary output) and
# the prokka gff files used for Roary and makes a gff file for the core genome alignment.
######

# check for correct arguments
if len(sys.argv) != 3:
    print("Usage: roaryToCoreGFF.py <core_alignment_header.embl> <gffdir/>")
    sys.exit(0)

embl = sys.argv[1]
gffdir = sys.argv[2]
coregff = embl.split(".")[0]+".gff"

# make a super gff file with a single copy of all annotations from all prokka gffs
#(not including hypotheticals)
annot = []
allgff = open("allGFF.gff", "w")

for file in os.listdir(gffdir):
    if file.endswith(".gff"):
        filename = gffdir+file
        with open(filename, "r") as f:
            for line in f:
                if "##FASTA" in line:
                    break
                elif not line.startswith("#"):
                    line = line.strip("\n")
                    info = line.split("\t")
                    annotation = info[8]
                    try:
                        if annotation.split(";")[3].startswith("gene"):
                            gene = annotation.split(";")[3].split("=")[1]
                            if gene.split("_")[0] not in annot:
                                allgff.write(line+"\n")
                                annot.append(gene.split("_")[0])
                        if annotation.split(";")[2].startswith("gene"):
                            gene = annotation.split(";")[2].split("=")[1]
                            if gene.split("_")[0] not in annot:
                                allgff.write(line+"\n")
                                annot.append(gene.split("_")[0])
                    except IndexError:
                        pass
allgff.close()

# convert core_alignment_header.embl to gff using to-gff
subprocess.call(["/opt/PepPrograms/to-gff/build/scripts-2.7/to-gff","--embl", embl, coregff])

# parse core gff into a list of genes
gfflist = []
with open(coregff, "r") as f:
    for line in f:
        if not line.startswith("#"):
            line = line.strip("\n")
            info = line.split("\t")
            if info[1] != "annotation":
                gene = ((info[8].split(";")[0]).split("=")[1])
                if not gene.startswith("group"):
                    gfflist.append(gene.split("_")[0].split("_")[0].split("_")[0].split("_")[0].split("_")[0].split("_")[0].split("_")[0].split("_")[0].split("_")[0])

# make dictionary of genes and annotations from compiled gff file
gffdict = {}
with open("allGFF.gff", "r") as f:
    for line in f:
        if "##FASTA" in line:
            break
        elif not line.startswith("#"):
            line = line.strip("\n")
            info = line.split("\t")
            annot = info[8]
            try:
                if annot.split(";")[3].startswith("gene"):
                    gene = annot.split(";")[3].split("=")[1]
                    if gene.split("_")[0] in gfflist:
                        gffdict[gene.split("_")[0]] = annot
                if annot.split(";")[2].startswith("gene"):
                    gene = annot.split(";")[2].split("=")[1]
                    if gene.split("_")[0] in gfflist:
                        gffdict[gene.split("_")[0]] = annot
            except IndexError:
                pass

# add additional information to core gff using gff dictionary
tempfile = coregff.split(".")[0]+".tmp"
tempout = open(tempfile, "w")

with open(coregff, "r") as f:
    for line in f:
            line = line.strip("\n")
            if not line.startswith("#"):
                info = line.split("\t")
                if info[1] != "annotation":
                    label = (info[8].split(";")[0])
                    gene = (((info[8].split(";")[0]).split("=")[1]).split("_")[0])
                    if gene in gffdict:
                        annotation = gffdict[gene]
                        tempout.write("\t".join(info[:8])+"\t"+";".join([label,annotation])+"\n")
                    else:
                        tempout.write(line+"\n")
                else:
                    tempout.write(line+"\n")
            else:
                tempout.write(line+"\n")

tempout.close()
os.rename("core_alignment_header.tmp", "core_alignment_header.gff")
os.remove("allGFF.gff")
