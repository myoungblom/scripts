#!/usr/bin/env python

import sys
import itertools
import os

#####
# This script takes a list of homoplasies from TreeTime and a gff and outputs the information
# with annotations added.
#####

# check for correct arguments
if len(sys.argv) != 3:
    print("Usage: homoplasyGeneCounts.py <homoplasies.csv> <annotations.gff>")
    sys.exit(0)

infile = sys.argv[1]
temp = infile.strip(".csv")+".tmp"
tempOut = open(temp, "w")
outFile = infile.strip(".csv")+"_annotated.csv"
gff = sys.argv[2]

results = []
homoDict = {}
geneDict = {}
homoCounts = {}

with open(infile, 'r') as f:
    print("processing homoplasy results ...")
    header = next(f)
    header = header.strip("\n")
    tempOut.write(header+",geneStart,geneStop,Strand,Annotation,PerGene\n")
    for line in f:
        tempOut.write(line)
        line = line.strip("\n")
        position = line.split(",")[0][1:-1]
        results.append(position)
tempOut.close()

print("Number of positions hit: "+str(len(results)))
print("Number of unique positions hit: "+str(len(set(results))))

with open(gff, 'r') as annot:
    print("matching homoplasies to genes ...")
    for line in annot:
        line = line.strip("\n")
        info = line.split("\t")
        start = int(info[3])
        stop = int(info[4])
        label = info[8].split(";")[0].split("=")[1]
        posList = list(range(start, stop+1))
        writeOut = ("%i,%i,%s,%s" % (start,stop, info[6], label))
	geneDict[writeOut] = 0
        for pos in posList:
            if str(pos) in results:
                homoDict[str(pos)] = writeOut
                geneDict[writeOut] += results.count(str(pos))

with open(outFile, "w") as out:
    with open(temp, 'r') as infile:
        print("writing output ...")
        out.write(next(infile))
        for line in infile:
            position = str(line.split(",")[0][1:-1])
            if position in homoDict.keys():
                annotation = homoDict[position]
		count = geneDict[annotation]
                out.write(line.strip("\n")+","+annotation+","+str(count)+"\n")
            else:
                out.write(line.strip("\n")+","+"intergenic"+"\n")
os.remove(temp)
