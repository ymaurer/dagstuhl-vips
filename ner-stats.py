#!/usr/bin/python
from argparse import ArgumentParser
import json

def dowork(args):
    lines = 0
    lines_with_ner = 0
    codes = [0,0,0,0,0]
    for f in args.file:
        with open(f, 'r') as fil:
            for line in fil:
                l = json.loads(line)
                lines = lines + 1
                found = False
                for i in l['ner_tags']:
                    codes[i] = codes[i] + 1
                    if i > 0:
                        found = True
                if found:
                    lines_with_ner = lines_with_ner + 1
    print(f"Number of lines: {lines}")
    print(f"Number of lines with at least one NE: {lines_with_ner}")
    st = 0
    for i in codes:
        print(f"Number of tokens with status {st}: {i}")
        st = st + 1

parser = ArgumentParser(description='parse a jsonl tokens / ner_tags file and extract statistics based on NER tags')
parser.add_argument('file', nargs='*', help='jsonl files')
args = parser.parse_args()
dowork(args)
