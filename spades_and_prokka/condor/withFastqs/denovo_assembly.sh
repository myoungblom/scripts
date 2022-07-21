#!/bin/sh

# fastqc
#/opt/PepPrograms/FastQC-0.11.8/fastqc $1_1.fastq.gz $1_2.fastq.gz -t 4

# running SPAdes
/opt/PepPrograms/SPAdes-3.13.1-Linux/bin/spades.py -1 $1_1.fastq.gz -2 $1_2.fastq.gz -t 8 -o $1_spades

# renaming & filtering output
mv $1_spades/scaffolds.fasta $1_spades/$1_scaffolds.fasta
python3 /opt/PepPrograms/contigFilter.py $1_spades/$1_scaffolds.fasta

# annotation
/opt/PepPrograms/prokka-1.14.0/bin/prokka --locustag $1 --prefix $1_annot --cpus 4 --genus $2 --species $3 --usegenus --rfam --gram $4 $1_spades/$1_scaffolds_filtered.fasta

mkdir output
mv * output/
zip -r $1_assembly.zip output/$1_spades
zip -r $1_annotation.zip output/$1_annot
