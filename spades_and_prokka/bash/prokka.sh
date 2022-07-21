#!/bin/sh

#Usage: script.sh IDlist.txt

while read f;
	do echo "$f";
	# running Prokka
	/opt/PepPrograms/prokka-1.14.0/bin/prokka --locustag "$f" --prefix "$f"_annot --cpus 2 --rfam "$f"_scaffolds_filtered.fasta
done < $1
