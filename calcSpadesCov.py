#!/usr/bin/env python3

import sys
from Bio import SeqIO

if len(sys.argv) < 4:
    print("Usage: script.py assembly.fasta read_length k-mer")
    sys.exit(0)

fastafile = sys.argv[1]
rlen = int(sys.argv[2])
kmer = int(sys.argv[3])

# read contig info into a dictionary
contigDict = {}
for contig in SeqIO.parse(fastafile, "fasta"):
    info = contig.id.split("_")
    contigDict[info[1]] = [int(info[3]),float(info[5])]

# calculate coverage per contig
outfile = fastafile.split(".")[0]+"_coverage.txt"
totallen = 0
totalcov = 0
with open(outfile,"w") as out:
    #out.write("contig\tlength\tcoverage\n")
    for contig, values in contigDict.items():
        cx = values[1] * (rlen/(rlen-kmer+1))
        totallen += values[0]
        totalcov += (cx*values[0])
        #out.write(contig+"\t"+str(values[0])+"\t"+str(cx)+"\n")

# average coverage across assembly
print(fastafile+" "+str(totalcov/totallen))
