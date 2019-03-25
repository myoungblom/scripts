scripts
=======

Scripts for various file manipulations & conversions.
Current Versions:
	Python 2.7.3
	Biopython 1.63

### contigLength.py
Ouputs length of contigs in a draft genome fasta file\
Requirements: Biopython\
Usage: contigLength.py <inputfile.fasta> <outputfile>

### mummerToFasta.py


### removeFromFasta.py
Removes specified sequence(s) from fasta file\
Requirements: Biopython\
Usage: removeFromFasta.py <inputfile.fasta> <output fasta> <ids or text file to remove>

### splitFasta.py
Splits multifasta file into individual fasta files\
Requirements: Biopython\
Usage: splitFasta.py <inputfile.fasta>

### pullFromFasta.py
Pulls specific sequences from multifasta file\
Requirements: Biopython\
Usage: pullFromFasta.py <inputfile.fasta> <ids or text file to remove>

### printSeq.py
Prints base at given position in fasta file sequence\
Requirements: Biopython\
Usage: printSeq.py <inputfile.fasta> <position>
