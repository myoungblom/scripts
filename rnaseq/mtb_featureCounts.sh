#!/bin/bash

regGTF="$1"
igrGTF="$2"
output="$3"
bams="${@:4}"

# fc 1
/opt/PepPrograms/subread-2.0.0-Linux-x86_64/bin/featureCounts -a ${regGTF}  -o ${output}_1_featureCounts -t transcript -g gene_id -p -T 4 ${bams}

# fc 2
#/opt/PepPrograms/subread-2.0.0-Linux-x86_64/bin/featureCounts -a ${regGTF}  -o ${output}_2_featureCounts -t transcript -g gene_id -p -T 4 -O --minOverlap 10 ${bams}

# fc 3
/opt/PepPrograms/subread-2.0.0-Linux-x86_64/bin/featureCounts -a ${igrGTF}  -o ${output}_3_featureCounts -t transcript -g gene_id -p -T 4 ${bams}

# fc 4
#/opt/PepPrograms/subread-2.0.0-Linux-x86_64/bin/featureCounts -a ${igrGTF}  -o ${output}_4_featureCounts -t transcript -g gene_id -p -T 4 -O --minOverlap 10 ${bams}

# summarize
python3 featureCountsSummary.py ${output}_1_featureCounts.summary \
	${output}_2_featureCounts.summary \
	${output}_3_featureCounts.summary \
	${output}_4_featureCounts.summary
