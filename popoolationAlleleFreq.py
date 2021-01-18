#!/usr/bin/env python

import sys


if len(sys.argv) != 4:
    print("Usage: popoolationAlleleFreq.py <#timepoints> <output_rc> <output.fet>")
    sys.exit(0)

points = int(sys.argv[1])
freq_file = sys.argv[2]
pval_file = sys.argv[3]
out_file = pval_file.split(".")[0]+"_popoolation.csv"

freq_dict = {}

with open(freq_file,"r") as IN:
    next(IN)
    for line in IN:
        line = line.strip()
        info = line.split("\t")
        pos = info[1]
        #ref = info[4].split("/")[0]
        #alt = info[4].split("/")[1]
        base = info[4]
        allele_counts = info[(-1*points):]
        freqs = []
        for x in allele_counts:
            count = int(x.split("/")[0])
            total = int(x.split("/")[1])
            freq = round((count/total)*100,0)
            freqs.append(freq)
        freq_dict[pos] = [base]+freqs

with open(pval_file,"r") as IN:
    for line in IN:
        line = line.strip()
        info = line.split("\t")
        pos = info[1]
        start_end = "1:"+str(points)+"="
        pvals = info[-1*points:]
        for x in pvals:
            if (x.startswith(start_end)) and (pos in freq_dict):
                freq_dict[pos].append(x.split("=")[1])


with open(out_file,"w") as out:
    for key,value in freq_dict.items():
        pos = str(key)
        newinfo = [pos]+[str(x) for x in value]
        newline = ",".join(newinfo)
        out.write(newline+"\n")

    

