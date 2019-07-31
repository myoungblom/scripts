#!/usr/bin/env python

import sys

# check for correct arguments
if len(sys.argv) != 2:
    print("Usage: roaryGPAtoRarefaction.py <roary_GPA.csv>")
    sys.exit(0)

gpa = sys.argv[1]
output = gpa.split(".")[0]+"_rarefaction.tsv"

# read csv, write out 1/0 presence/absence file
out = open(output, 'w')

with open(gpa, 'r') as f:
    next(f)
    for line in f:
        writeOut = []
        line = line.strip("\n")
        info = line.split(",")
        for i in info:
            if i == "":
                writeOut.append("0")
            else:
                writeOut.append("1")
        out.write("\t".join(writeOut)+"\n")

out.close()
