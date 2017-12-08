# CRISPR

An efficient command-line tool for CRISPR-CAS9 experiment design.

## How to test it out
The below commands can help you quickly test our tool out on the phi-x virus

~~~~
Build the indices:
python src/krispr_kreme.py build -p Phi-Genome

Query a short sequence:
python src/krispr_kreme.py query -s "GATATGAGTCACATTTTGTT" -p Phi-Genome -o alignments-phi.json

Score the outputs:
python src/krispr_kreme.py score -s "GATGCTGTTCAACCACTAAT" -i alignments-phi.json -o output-phi.json
~~~~

