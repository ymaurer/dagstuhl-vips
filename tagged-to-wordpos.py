#!/usr/bin/python
from argparse import ArgumentParser
import spacy
import json

def dowork(args):
    print(args.file[0])
    print(args.file[1])


parser = ArgumentParser(description='Parse textblock jsonl files and combine them using the tagged words to generate named-entity based jsonl')
parser.add_argument('file', nargs=2, help='textblock jsonl & tagged sentence jsonl')
args = parser.parse_args()
dowork(args)
