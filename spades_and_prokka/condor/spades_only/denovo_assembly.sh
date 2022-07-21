#!/bin/sh

# running SPAdes
/opt/PepPrograms/SPAdes-3.13.1-Linux/bin/spades.py -1 $1_1.fastq.gz -2 $1_2.fastq.gz -t 8 -o $1_spades

# filtering contigs for length and coverage
mv $1_spades/scaffolds.fasta $1_spades/$1_scaffolds.fasta
python contig_filter.py $1_spades/$1_scaffolds.fasta 

mkdir output
mv *_spades output/
zip -r $1_assembly.zip output/$1_spades
