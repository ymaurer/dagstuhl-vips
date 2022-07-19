#!/usr/bin/python
from argparse import ArgumentParser
import json

def dowork(args):
    lines = 0
    lines_with_ner = 0
    codes = {}
    cooccurences = [[0,0],[0,0]]
    for f in args.file:
        with open(f, 'r') as fil:
            for line in fil:
                l = json.loads(line)
                lines = lines + 1
                found = False
                oc_hidden = 0
                oc_public = 0
                for i in l['ner_tags']:
                    if not i in codes:
                        codes[i] = 0
                    codes[i] = codes[i] + 1
                    if i != 'O':
                        found = True
                    if i.endswith('HIDDEN'):
                        oc_hidden = 1
                    if i.endswith('PUBLIC'):
                        oc_public = 1
                if found:
                    lines_with_ner = lines_with_ner + 1
                cooccurences[oc_hidden][oc_public] = cooccurences[oc_hidden][oc_public] + 1
    print(f"Number of lines: {lines}")
    print(f"Number of lines with at least one NE: {lines_with_ner}")
    for i in codes:
        print(f"Number of tokens with status {i}: {codes[i]}")
    print(f"Total Number of entites: {codes['B-PUBLIC']+codes['B-HIDDEN']}")
    print(f"Number of lines with only HIDDEN named entites: {cooccurences[1][0]}")
    print(f"Number of lines with only PUBLIC named entites: {cooccurences[0][1]}")
    print(f"Number of lines with only both HIDDEN and PUBLIC named entites: {cooccurences[1][1]}")

parser = ArgumentParser(description='parse a jsonl tokens / ner_tags file and extract statistics based on NER tags')
parser.add_argument('file', nargs='*', help='jsonl files')
args = parser.parse_args()
dowork(args)
