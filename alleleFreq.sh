#! bin/bash

#####
# This script serves the same function as breseq and gdtools compare - input is a 
# a reference, a bed file of regions to exclude and a set of bams
# from a single strain sequenced at different time points. Output is a csv of mutation frequencies
# across those time points. Also requires companion python script "alleleFreq.py"
#####

# usage: alleleFreq.sh <path.to.ref> <bed> <bam1> <bam2> ... <bamN>

ref="$1"
bed="$2"
bams="${@:3}"

# compile mutations from bam files
for x in ${bams}
do
    bcftools mpileup -f ${ref} -o ${x/.bam/.vcf} -O v -a AD,ADF,ADR ${x}
done

# filter out low quality mutations
for x in ${bams}
do
    bcftools filter -s LowQual -e "%QUAL<20 || DP>100" ${x/.bam/.vcf} > ${x/.vcf/.flt.vcf}
done

