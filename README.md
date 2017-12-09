# KrisprKreme

An efficient command-line tool for CRISPR-CAS9 experiment design.

## Usage

The following steps were successfully executed in an Ubuntu Box - 64-bit 16.04 Xenial.

**Step 1**:
Install the tool dependencies using
```
$ pip install -r requirements.txt
```

**Step 2**:
Download the Gemtools aligner binaries from http://gemtools.github.io and add the Gemtools' `bin` folder to `$PATH`

**Step 3**:
Download and install the ViennaRNA package from https://www.tbi.univie.ac.at/RNA

**Step 4**:
For the scoring Machine Learning model we have the unfeaturied data in `src/model/processed.json`. This has to be converted to
one-hot encoded featurized csv. In order to do that run
```
$ python src/model/featurize.py
```
**Note**: This will take some time

**Step 5**:
Now that the data is featurized we need to create the Random Forest model by doing
```
$ python src/model/scoring_model.py create_model
```

**Step 6**:
To easily test out a smaller genome, we have added the phi-X virus genome to source code in `Phi-Genome` folder. To build Bloom
and GEM indices for this
```
$ python krispr_kreme.py build -p Phi-Genome
```

**Step 7**:
To querying step happens in 2 steps:
    1. The 20nt sgRNA sequence is queried in the Bloom Filter indices of all chunks (for phi-X virus it is only one chunk but for human genome each chunk is a chromosome).
    2. The sequence is then aligned using GEM indices of only the chunks obtained from the previous step because only in those chunks the sequence is found.

    To do this, run
    ```
    $ python src/krispr_kreme.py query -s "GATGCTGTTCAACCACTAAT" -p Phi-Genome -o alignments-phi.json
    ```

**Step 8**:
To do on-target and off-target scoring of the output of the query and alignment steps run
```
$ python src/krispr_kreme.py score -s "GATGCTGTTCAACCACTAAT" -p alignments-phi.json -o output-phi.json
```

## Machine Learning Model Evaluation

To plot the ROC and Precision-Recall curves for the SVM model and the Random Forest model run
```
$ python src/model/scoring_model.py plot_curves
```

## Deep Learning Model Evaluation

To run the training/validation process of the Deep Convolution Neural Network follow these steps:

Install Caffe by following the instructions https://github.com/BVLC/caffe/wiki/Ubuntu-16.04-or-15.10-Installation-Guide. Use the
CPU mode of Caffe and make sure you do `export $PATH=<caffe-root-path>/build/tools/:$PATH`. To train the network

```
$ cd src/model/cnn
$ caffe train --solver=sgrna-dcnn-solver.prototxt
```
