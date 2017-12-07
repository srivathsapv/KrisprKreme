# CRISPR

An efficient command-line tool for CRISPR-CAS9 experiment design.

## How to test it out
The below commands can help you quickly test our tool out on the phi-x virus

~~~~
Build the indices:
python src/crispy_creme.py build -p Phi-Genome

Query a short sequence:
python src/crispy_creme.py query -s "GATATGAGTCACATTTTGTT" -p Phi-Genome -o alignments-phi.json

Score the outputs:
python src/crispy_creme.py score -s "GATGCTGTTCAACCACTAAT" -i alignments-phi.json -o output-phi.json
~~~~

