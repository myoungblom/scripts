#!/usr/bin/env python

import sys
from gff3 import Gff3
from Bio import SeqIO
from Bio.SeqUtils import GC

#####
# This script takes in a single contig genome, and the corresponding GFF file
# and returns the average GC content of all genes and the intergenic regions.
#####

# check for correct arguments
if len(sys.argv) != 3:
    print("Usage intergenicGC.py <genome.fasta> <annotation.gff>")
    sys.exit (0)

genome = sys.argv[1]
annotation = sys.argv[2]
outFileName = genome.split(".")[0]+"_intergenicGC.txt"

# parse GFF file into genes and intergenic regions
genomeRecord = next(SeqIO.parse(genome, "fasta"))
genomeSeq = str(genomeRecord.seq)
lastEnd = 0
geneNum = 1
genes = ""
intergenic = ""

gff = Gff3()
gff.parse(annotation)
gff.parse_fasta_external(genome)







with open(annotation, 'r') as annot:
    for line in annot:
        if not line.startswith("#"):
            line = line.strip()
            info = line.split("\t")
            region = info[2]
            if region == "gene":
                start = int(info[3])
                end = int(info[4])
                geneSeq = genomeSeq[start-1:end]
                print(geneSeq)
                genes = genes.join(geneSeq) 
                 


# write output file
# number of genes
    # avg gene GC + SD
# avg intergenic GC + SD
