#!/usr/bin/env python

#####
# Takes in a file with a list of positions of interest and a gff, returns
# a file with annotations for those positions.
#####

import sys
import itertools
import os

# check for correct arguments
if len(sys.argv) != 3:
    print("Usage: SVresultsGenes.py <SVOutput.csv> <annotations.gff>")
    sys.exit(0)

# name various files
svfile = sys.argv[1]
temp = svfile.split(".")[0]+".tmp"
tempOut = open(temp, "w")
outFile = svfile.strip(".csv")+"_annotated.csv"
gff = sys.argv[2]

# write to temporary file and make list of positions of interest
svs = []
SVDict = {}
with open(svfile, 'r') as f:
    header = next(f).strip("\n")
    tempOut.write(header+",geneStart,geneStop,Strand,Annotation\n")
    for line in f:
        tempOut.write(line)
        svs.append(line.strip("\n").strip("\r"))
tempOut.close()

# write annotations into a dictionary based on positions of interest
with open(gff, 'r') as annot:
    for line in annot:
        if not line.startswith("#"):
            line = line.strip("\n")
            info = line.split("\t")
            start = int(info[3])
            stop = int(info[4])
            posList = list(range(start, stop+1))
            writeOut = ("%i,%i,%s,%s" % (start,stop, info[6], info[8]))
            for pos in posList:
                if str(pos) in svs:
                    SVDict[str(pos)] = writeOut

# write annotations to output file
with open(outFile, "w") as out:
    for item in svs:
        if item in SVDict.keys():
            annotation = SVDict[item]
            out.write(line.strip("\n")+","+annotation+"\n")
        else:
            out.write(line.strip("\n")+","+"intergenic"+"\n")
os.remove(temp)
