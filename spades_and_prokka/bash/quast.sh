#!/bin/bash

#Usage: script.sh

for f in *_spades;
	do /opt/PepPrograms/quast-5.0.2/quast.py -o ./${f/_spades/_quast} $f/*scaffolds_filtered.fasta;
done

