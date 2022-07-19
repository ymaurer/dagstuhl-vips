#!/usr/bin/python
from argparse import ArgumentParser
import json

def dowork(args):
    for f in args.file:
        with open(f, 'r') as fil:
            for line in fil:
                l = json.loads(line)
                found = False
                for i in l['ner_tags']:
                    if i != 'O':
                        found=True
                        break
                if found and args.onlyner:
                    print(line.strip())

parser = ArgumentParser(description='parse a jsonl tokens / ner_tags file and filter based on presence of NER tags')
parser.add_argument('--onlyner', action='store_true', help='filter only lines that contain at least one named entity')
parser.add_argument('file', nargs='*', help='jsonl files')
args = parser.parse_args()
dowork(args)
