#!/usr/bin/env python3

import sys
from collections import defaultdict

#####
# Parses featureCounts summaries.
#####

if len(sys.argv) != 5:
    print("Usage: script.py featureCounts1 fC2 fC3 fC4")
    sys.exit(0)

f1 = sys.argv[1]
#f2 = sys.argv[2]
f3 = sys.argv[3]
#f4 = sys.argv[4]
outfile = f1.split("_")[0]+"_featureCountsParsed.csv"


# genes = 1a (f1,assigned) 
# igrs = 1b (f1,no feature)
# overlapping = 1c (f1,ambiguous), 3c (f3,ambiguous)

readCounts = defaultdict(int)
with open(f1,"r") as f:
    isolates = next(f).split("\t")[1:]
    for line in f:
        count = 0
        info = line.strip().split("\t")
        status = info[0]
        if not status == "Unassigned_Unmapped":
            for x in info[1:]:
                iso = isolates[count].strip()
                readCounts[iso] += int(x)
                count += 1
for key,value in readCounts.items():
    readCounts[key] = value/1000000

def parseFc(filename, readtype):
    outDict = defaultdict(int)
    with open(filename, "r") as f:
        isolates = next(f).split("\t")[1:]
        for line in f:
            count = 0
            info = line.strip().split("\t")
            status = info[0]
            if status == readtype:
                for x in info[1:]:
                    iso = isolates[count].strip()
                    outDict[iso] = x
                    count += 1
    return outDict

a1 = parseFc(f1, "Assigned")
b1 = parseFc(f1, "Unassigned_NoFeatures")
c1 = parseFc(f1, "Unassigned_Ambiguity")
c3 = parseFc(f3, "Unassigned_Ambiguity")

header = "Sample,Genes,IGRs,Overlapping-1,Overlapping-2"
with open(outfile,"w") as out:
    out.write(header+"\n")
    for key,value in a1.items():
        a_1 = round(int(a1[key])/readCounts[key])
        b_1 = round(int(b1[key])/readCounts[key])
        c_1 = round(int(c1[key])/readCounts[key])
        c_3 = round(int(c3[key])/readCounts[key])
        newline = [key,str(a_1),str(b_1),str(c_1),str(c_3)]
        out.write(",".join(newline)+"\n")

