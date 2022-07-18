# dagstuhl-vips
programs and data from the Dagstuhl seminar on Computational Approaches for digitized newspapers working group 1.

## ner2json.py
```
usage: ner2json.py [-h] [--sonar] [file ...]

parse a tsv NER file and transform it into tokenized sequence

positional arguments:
  file        tsv tagged file(s)

optional arguments:
  -h, --help  show this help message and exit
  --sonar     SONAR-type tagging with I-PER / B-PER in column 2 and NIL / Qxxxx in column 8
```