#!/usr/bin/env python3

import sys
from collections import defaultdict

#####
#
#####

if len(sys.argv) != 2:
    print("Usage: script.py featureCountsFilename")
    sys.exit(0)

countsfile = sys.argv[1]
outfile = countsfile+"_normalized"
summaryfile = countsfile+".summary"

readCounts = defaultdict(int)

with open(summaryfile,"r") as f:
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

with open(countsfile, "r") as f:
    with open(outfile, "w") as out:
        out.write(next(f))
        for line in f:
            if line.startswith("Geneid"):
                out.write(line)
                isolates = line.strip().split("\t")[6:]
            else:
                info = line.strip().split("\t")
                newline = info[:6]
                count = 0
                for x in info[6:]:
                    iso = isolates[count]
                    norm = readCounts[iso]/1000000
                    normCount = round(float(x)/float(norm))
                    newline.append(normCount)
                    count += 1
                out.write("\t".join([str(x) for x in newline])+"\n")
