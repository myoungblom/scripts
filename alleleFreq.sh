#! bin/bash

#####
# This script serves the same function as breseq and gdtools compare - input is a 
# a reference, a bed file of regions to exclude and a set of bams
# from a single strain sequenced at different time points. Output is a csv of mutation frequencies
# across those time points. Also requires companion python script "alleleFreq.py"
#####

# usage: alleleFreq.sh <strain.name> <path.to.ref> <bed> <bam1> <bam2> ... <bamN>

strain="$1"
ref="$2"
bed="$3"
bams="${@:4}"

# compile mutations from bam files & filter out low quality muts
for x in ${bams};
do
    echo ${x};
    bcftools mpileup -f ${ref} -o ${x/.bam/.vcf} -O v -a AD,ADF,ADR ${x};
    bcftools filter -s LowQual -e "%QUAL<20 || DP>100" ${x/.bam/.vcf} > ${x/.bam/.flt.vcf};
done

vcfs=(*.flt.vcf)
echo ${vcfs[*]}

# run python script to tabulate & filter mutations
python3 alleleFreq.py ${strain} ${bed} ${vcfs[*]}
