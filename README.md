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

## ner-stats.py
```
usage: ner-stats.py [-h] [file ...]

parse a jsonl tokens / ner_tags file and extract statistics based on NER tags

positional arguments:
  file        jsonl files

optional arguments:
  -h, --help  show this help message and exit
```
## filter-ner.py
```
usage: filter-ner.py [-h] [--onlyner] [file ...]

parse a jsonl tokens / ner_tags file and filter based on presence of NER tags

positional arguments:
  file        jsonl files

optional arguments:
  -h, --help  show this help message and exit
  --onlyner   filter only lines that contain at least one named entity
``` 

## Label encoding
 - 0: Outside of PERSON
 - 1: B-PUBLIC Begin of public person mention with a wikidata QID
 - 2: I-PUBLIC Inside a public person mention with a wikidata QID
 - 3: B-HIDDEN Begin of a person mention without a wikidata QID (NIL link)
 - 4: I-HIDDEN Inside a person mention without a wikidata QID (NIL link)
 
