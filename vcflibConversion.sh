#!/bin/bash

# vcflibFst.sh <snps.vcf> <target isolates> <background isolates>

/opt/PepPrograms/vcflib/bin/wcFst --type GT --target echo "$(cat $2)" --background echo "$(cat $3)" --file $1
