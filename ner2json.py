#!/usr/bin/python
from argparse import ArgumentParser
import json

def output_textline(textline):
    if len(textline['tokens']) > 1:
        print(json.dumps(textline))

def reset_textline():
    textline = {}
    textline["tokens"] = []
    textline["ner_tags"] = []
    return textline

def class_sonar(col):
    if col[1] == 'B-PER':
        if col[7] == 'NIL':
            return 'B-HIDDEN'
        else:
            return 'B-PUBLIC'
    elif col[1] == 'I-PER':
        if col[7] == 'NIL':
            return 'I-HIDDEN'
        else:
            return 'I-PUBLIC'
    return 'O'

def class_hipe2020(col):
    if col[1] == 'B-pers':
        if col[5] == 'B-comp.name' or col[5] == 'O':
            if col[7] == 'NIL':
                return 'B-HIDDEN'
            else:
                return 'B-PUBLIC'
    elif col[1] == 'I-pers':
        if col[7] == 'NIL':
            return 'I-HIDDEN'
        else:
            return 'I-PUBLIC'
    return 'O'

def dowork(args):
    for f in args.file:
        with open(f,"r") as fil:
            textline = reset_textline()
            for line in fil:
                if len(line) > 1:
                    if line[0:1] == '#':
                        output_textline(textline)
                        textline = reset_textline()
                    else:
                        col = line.split()
                        textline['tokens'].append(col[0])
                        if args.dataset == 'sonar':
                            textline['ner_tags'].append(class_sonar(col))
                        if args.dataset == 'hipe2020':
                            textline['ner_tags'].append(class_hipe2020(col))
                        if col[9]=='EndOfSentence':
                            output_textline(textline)
                            textline = reset_textline()



parser = ArgumentParser(description='parse a tsv NER file and transform it into tokenized sequence')
parser.add_argument('--dataset', action='store', help='sonar: SONAR-type tagging with I-PER / B-PER in column 2 and NIL / Qxxxx in column 8, hipe2020')
parser.add_argument('file', nargs='*', help='tsv tagged file(s)')
args = parser.parse_args()
dowork(args)
