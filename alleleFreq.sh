#! bin/bash


bcftools mpileup -f /opt/data/mtuberculosis/MtbNCBIH37Rv.fa -o test.vcf -O v -a AD,ADF,ADR ERR003120.realn.bam

bcftools filter -s LowQual -e "%QUAL<20 || DP>100" test.vcf > test.flt.vcf