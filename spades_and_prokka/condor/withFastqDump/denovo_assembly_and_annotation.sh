#!/bin/sh

/opt/PepPrograms/SPAdes-3.13.0-Linux/bin/spades.py -1 $1_1.fastq -2 $1_2.fastq -t 8 -o $1_spades
/opt/PepPrograms/prokka-1.12/bin/prokka --locustag $1 --prefix $1_annot --cpus 8 --genus $2 --species $3 --usegenus $1_spades/scaffolds.fasta
mkdir output
mv * output/
zip -r $1_assembly.zip output/$1_spades
zip -r $1_annotation.zip output/$1_annot
