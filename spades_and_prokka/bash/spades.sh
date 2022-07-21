#!/bin/sh

#Usage: script.sh IDlist.txt

while read f;
	do echo "$f";
	# running SPAdes
	/opt/PepPrograms/SPAdes-3.13.1-Linux/bin/spades.py -1 "$f"_1.fastq.gz -2 "$f"_2.fastq.gz -t 8 -o "$f"_spades &> "$f"_spades.log;
	# renaming output fasta file
	mv "$f"_spades/scaffolds.fasta "$f"_spades/"$f"_scaffolds.fasta;
	# python script which filters out bad contigs
	python3 contigFilter.py "$f"_spades/"$f"_scaffolds.fasta;
done < $1
