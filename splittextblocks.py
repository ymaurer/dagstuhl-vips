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
                token_counter = 0
                token_length = 0
                for sentence in doc.sents:
                    print(json.dumps({'id': j['id'] + '/position/' + str(counter), 'text': sentence.text}))
                    # add tokens until we get to counter + len(sentence)
                    while token_counter < len(j['tokens']) and token_length < counter + len(sentence.text):
                        # add length of token and space following it
                        token_length += len(j['tokens'][token_counter]) + 1
                        token_counter = token_counter + 1
                    if token_counter == len(j['tokens']) and token_length < counter + len(sentence.text):
                        print('ERROR: are there tokens missing?')
                    if token_length > counter + len(sentence.text) + 1:
                        # remove last token we added, since spacy has split that between sentences
                        token_counter = token_counter - 1
                        # remove the length of the token and the space
                        token_length -= len(j['tokens'][token_counter]) + 1
                        # calculate how long the left part of the token is that is in the previous sentence
                        left_token = counter + len(sentence.text) - token_length
                        # cut the token so that we still have the coordinates (careful, this prevents you from running the algorithm twice on a line)
                        j['tokens'][token_counter] = j['tokens'][token_counter][left_token:]
                        token_length = token_length + left_token
                        # do not add a space
                        counter += len(sentence.text)
                    else:
                        # add length of sentence and space
                        counter += len(sentence.text) + 1

parser = ArgumentParser(description='Parse textblock jsonl files and split them into sentences using spacy')
parser.add_argument('--lang', default='fr', action='store', help='Language (default=fr)')
parser.add_argument('file', nargs='*', help='jsonl files')
args = parser.parse_args()
dowork(args)
