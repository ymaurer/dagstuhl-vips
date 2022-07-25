#!/usr/bin/python
from argparse import ArgumentParser
import spacy
import json

models = {'fr': 'fr_core_news_sm'}

def dowork(args):
    nlp = spacy.load(models[args.lang], exclude=["parser"])
    nlp.enable_pipe("senter")
    for f in args.file:
        with open(f, 'r') as fil:
            for line in fil:
                j = json.loads(line)
                txt = ' '.join(j['tokens'])
                doc = nlp(txt)
                counter = 0
                for sentence in doc.sents:
                    print(json.dumps({'id': j['id'] + '/position/' + str(counter), 'text': sentence.text}))
                    counter += len(sentence.text) + 1

parser = ArgumentParser(description='Parse textblock jsonl files and split them into sentences using spacy')
parser.add_argument('--lang', default='fr', action='store', help='Language (default=fr)')
parser.add_argument('file', nargs='*', help='jsonl files')
args = parser.parse_args()
dowork(args)
