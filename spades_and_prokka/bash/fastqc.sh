#!/bin/bash

# Usage: script.sh IDlist.txt

while read f;
	do echo "$f";
	/opt/PepPrograms/FastQC-0.11.8/fastqc -t 2 "$f"_1.fastq.gz "$f"_2.fastq.gz &>> fastqc.log;
done < $1
