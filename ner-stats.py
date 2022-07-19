#!/usr/bin/python
from argparse import ArgumentParser
import json

def dowork(args):
    lines = 0
    lines_with_ner = 0
    codes = {}
    for f in args.file:
        with open(f, 'r') as fil:
            for line in fil:
                l = json.loads(line)
                lines = lines + 1
                found = False
                for i in l['ner_tags']:
                    if not i in codes:
                        codes[i] = 0
                    codes[i] = codes[i] + 1
                    if i != 'O':
                        found = True
                if found:
                    lines_with_ner = lines_with_ner + 1
    print(f"Number of lines: {lines}")
    print(f"Number of lines with at least one NE: {lines_with_ner}")
    for i in codes:
        print(f"Number of tokens with status {i}: {codes[i]}")

parser = ArgumentParser(description='parse a jsonl tokens / ner_tags file and extract statistics based on NER tags')
parser.add_argument('file', nargs='*', help='jsonl files')
args = parser.parse_args()
dowork(args)
