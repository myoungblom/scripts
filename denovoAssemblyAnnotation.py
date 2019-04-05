#!usr/bin/env python

import sys
import os



#####
# This script takes in a text file of NCBI-SRA id's and sequence information,
# downloads the fastq files,assembles the genomes with SPAdes, QC's the assemblies
# with QUAST and annotates the resulting contigs with prokka.
#####

# Format for tab-separated input file:
# SRA_ID	Genus	species

# check for correct commandline arguments
if len(sys.argv) != 2:
	print("Usage: denovoAssemblyAnnotation.py inputfile.txt")
	sys.exit(0)


/opt/PepPrograms/sratoolkit.2.9.2-ubuntu64/bin/fastq-dump.2.9.2 --split-files {ID}
/opt/PepPrograms/FastQC-0.11.8/fastqc -t 4 {ID}_1.fastq {ID}_2.fastq
/opt/PepPrograms/SPAdes-3.13.0-Linux/bin/spades.py -t 8 -o {ID}_spades -1 {ID}_1.fastq -2 {ID}_2.fastq
/opt/PepPrograms/quast-5.0.2/quast.py {ID}_spades/scaffolds.fasta -o {ID}_quast
/opt/PepPrograms/prokka-1.12/bin/prokka --locustag {ID} --prefix {ID}_annot --cpus 8 --genus {Genus} --species {species} {ID}_spades/scaffolds.fasta
