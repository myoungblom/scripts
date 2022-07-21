#!/bin/bash

# Usage: script.sh IDlist.txt

while read f;
	do echo "$f";
	java -jar /opt/PepPrograms/Trimmomatic-0.39/trimmomatic-0.39.jar PE "$f"_1.fastq.gz "$f"_2.fastq.gz -baseout "$f".fq.gz -threads 4 ILLUMINACLIP:/opt/PepPrograms/bbmap/resources/adapters.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:50;
done < $1	
