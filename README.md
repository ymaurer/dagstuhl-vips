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

## extract-alto-blocks.py
```
usage: extract-alto-blocks.py [-h] [file ...]

Parse METS/ALTO files and extract textblocks from ALTO with coordinates

positional arguments:
  file        mets files

optional arguments:
  -h, --help  show this help message and exit
```
Its output format is the following:
```json
{
  "id": "https://persist.lu/ark:70795/7zc8m0/pages/1/textblock/ART2-1",
  "tokens": [
    "L’Allemagne",
    "et",
    "le",
    "désarmement"
  ],
  "token_coords": [
    {
      "x": "214",
      "y": "886",
      "w": "511",
      "h": "66"
    },
    {
      "x": "767",
      "y": "882",
      "w": "83",
      "h": "58"
    },
    {
      "x": "893",
      "y": "882",
      "w": "71",
      "h": "58"
    },
    {
      "x": "1004",
      "y": "881",
      "w": "587",
      "h": "59"
    }
  ],
  "page": 1,
  "page_height": "4957",
  "page_width": "3478",
  "ARK": "https://persist.lu/ark:70795/7zc8m0",
  "paperid": "indeplux",
  "date": "1928-01-01",
  "numpages": 4
}
```
## splittextblocks.py
```
usage: splittextblocks.py [-h] [--lang LANG] [file ...]

Parse textblock jsonl files and split them into sentences using spacy

positional arguments:
  file         jsonl files

optional arguments:
  -h, --help   show this help message and exit
  --lang LANG  Language (default=fr)
```
The output format is the following:
```json
{
  "id": "https://persist.lu/ark:70795/7zc8m0/pages/1/textblock/ART2-1/position/0",
  "text": "L’Allemagne et le désarmement"
}
```
## Label encoding
 - 0: Outside of PERSON
 - 1: B-PUBLIC Begin of public person mention with a wikidata QID
 - 2: I-PUBLIC Inside a public person mention with a wikidata QID
 - 3: B-HIDDEN Begin of a person mention without a wikidata QID (NIL link)
 - 4: I-HIDDEN Inside a person mention without a wikidata QID (NIL link)
 
