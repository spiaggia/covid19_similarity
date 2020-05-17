# covid19_similarity

This is the natural language processing etude, not science.

## Usage

- this code will run on Python 3.7.3.

```bash
$ python --version
Python 3.7.3
```

- setup natural language module

```bash
$ pip install python-Levenshtein
```
- git clone this repository

```bash
$ git clone https://github.com/spiaggia/covid19_similarity.git
$ cd covid19_similarity

```

- visit downlod sequence site

  - https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/virus?VirusLineage_ss=Severe%20acute%20respiratory%20syndrome%20coronavirus%202%20(SARS-CoV-2),%20taxid:2697049&SeqType_s=Nucleotide

- check all nucleotides

- download "Sequence data(FASTA Format) Nucleotide"
```bash
$ ls
README.md
covid_similarity.py	sequences.fasta
```

- execute covid_similarity.py

```bash
$ python covid_similarity.py
```

# References

- [Python]文字列の類似度計算3つの手法を実装・比較
  - http://pixelbeat.jp/text-matching-3-approach-with-python/#toc_id_1
