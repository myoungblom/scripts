#!/bin/bash

# Usage: script.sh IDlist.txt

while read f;
	do echo "$f";
	# running kraken
	/opt/PepPrograms/kraken2/kraken2 --db /opt/PepPrograms/kraken2/03.27.2019_bactDB/ --gzip-compressed --paired "$f"_1.fastq.gz "$f"_2.fastq.gz --output "$f"_kraken_out.txt --report "$f"_kraken_report.txt --use-names;
done < $1
