#! bin/bash

#####
# Usage: run_popoolation.sh <strain_name> <path/to/ref> <path/to/bed> <bam1> ... <bamN>
#####

strain="$1"
ref="$2"
bed="$3"
bams="${@:4}"

# make mpileup file
echo "Creating mpileup file ..."
/opt/PepPrograms/samtools-1.11/bin/samtools mpileup -B -f ${ref} -o ${strain}.mpileup ${bams}

# convert mpileup file to sync
echo "Converting mpilup file to sync file ..."
java -ea -Xmx7g -jar /opt/PepPrograms/popoolation2_1201/mpileup2sync.jar --input ${strain}.mpileup --output ${strain}.sync --fastq-type sanger --min-qual 20 --threads 8

# use python script to convert sync file to TSV
python3 ~/scripts/scripts/popoolationSynctoTSV.py --bed ${bed} --min-count 5 --min-coverage 20 --min-freq 5 --output ${strain}_popoolation.tsv ${strain}.sync
