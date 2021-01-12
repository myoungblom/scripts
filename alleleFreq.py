#!/usr/bin/env python

import sys

#####
# Companion script to alleleFreq.sh, takes in filtered vcf files from
# a single isolate sequenced at multiple time points, and tabulates
# mutation frequencies at each point.
# Filters:
#   - filters out mutations in regions specified by bed file
#   - filters out fixed mutations relative to the reference
#####

if len(sys.argv) < 4:
	print("Usage: alleleFreq.py <strain.name> <bed file> <vcf1> <vcf2> ... <vcfN")
	sys.exit(0)

strain = sys.argv[1]
bed = sys.argv[2]
vcfs = sys.argv[3:]


def getBedCoor(bedfile):
    bedCoor = []
    with open(bedfile, "r") as f:
        for line in f:
            line = line.strip()
            info = line.split("\t")
            for i in range(int(info[1]), int(info[2])+1):
                bedCoor.append(i)
    return(bedCoor)

bad_coordinates = getBedCoor(bed)

def filterMuts(vcf, dict_out, filter):
    with open(vcf,"r") as f:
        print(vcf)    
        for line in f:                    
            if not line.startswith("#"):  
                line = line.strip()
                info = line.split("\t")
                pos = info[1]
                #if pos not in filter:
                ref = info[3]
                alt = info[3]
                counts = info[9]
                alleles = counts.split(":")[3]
                refC = int(alleles.split(",")[0])
                altC = int(alleles.split(",")[1])
                #if (int(altC) > 5):
                total = ref+alt
                print(refC,altC,total)
                refF = round((refC/total)*100,0)
                altF = round((altC/total)*100,0)
                dict_out[str(pos)+alt] = [altF]
    print(dict_out)
    return dict_out

freqs = {}
header = ["position","ref","alt"]

for x in vcfs:
    header.append(x.split(".")[0])
    filterMuts(x, freqs, bad_coordinates)