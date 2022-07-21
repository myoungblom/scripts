#!/bin/bash

# Usage: script.sh IDlist.txt

while read f;
	do echo "$f";
	/home/myoungblom/sratoolkit.3.0.0-ubuntu64/bin/fasterq-dump -S -m 1G -e 8 "$f" &>> fasterq-dump.log;
	gzip "$f"_1.fastq;
	gzip "$f"_2.fastq;
done < $1
