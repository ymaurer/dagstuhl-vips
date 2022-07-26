#!/usr/bin/python
from argparse import ArgumentParser
import json
import re
import math

textblocks = {}

def read_textblocks(f):
    with open(f, 'r') as fil:
        for line in fil:
            j = json.loads(line)
            textblocks[j['id']] = j

def centroid(box):
    return {'x': int(box['x']) + int(box['w'])/2, 'y': int(box['y']) + int(box['h'])/2 }

def rescale(coord, width, height):
    return {'x': int(coord['x'])/int(width), 'y': int(coord['y'])/int(height)}

def project(coord):
    return math.sqrt((coord['x']+coord['y'])/2)

def read_sentences(f):
    with open(f, 'r') as fil:
        for line in fil:
            j = json.loads(line)
            m = re.match('^(.*)\/position\/(\d+)$', j['id'])
            tbid = m.group(1)
            offset = int(m.group(2))
            tb = textblocks[tbid]
            out = {
                'paperid': tb['paperid'],
                'date': tb['date'],
                'page': tb['page'],
                'numpages': tb['numpages'],
            }
            token_length = 0
            i = 0
            # skip to the first token of the textblock for this sentence
            while token_length < offset and i < len(tb['tokens']):
                token_length += len(tb['tokens'][i]) + 1
                i += 1
            # check if we ended up in the middle of a token. This can happen if spacy split a token into distinct sentences
            if token_length > offset:
                # go back one token
                i = i - 1
                # take off last token and space
                token_length -= len(tb['tokens'][i]) + 1
                # split last token (HACK, do not do this)
                left_token = offset - token_length
                tb['tokens'][i] = tb['tokens'][i][left_token:]
                token_length += left_token
            # output the sentence and its tokens
            slen = 0
            entity_index = 0
            while slen < len(j['text']) and entity_index < len(j['pos']):
                # Check whether we are on a person
                if slen >= j['pos'][entity_index][0]:
                    # only take into account beginning of person named entities
                    if j['tags'][entity_index].startswith('B-'):
                        # calculate coordinates of the center and project it against the diagonal
                        pos = rescale(centroid(tb['token_coords'][i]), tb['page_width'], tb['page_height'])
                        out['coord_x'] = pos['x']
                        out['coord_y'] = pos['y']
                        out['diag_pos_page'] = project(pos)
                        out['diag_pos_issue'] = out['diag_pos_page'] / int(tb['numpages']) + (int(tb['page']-1)/int(tb['numpages']))
                        out['text'] = tb['tokens'][i]
                        out['ne_type'] = j['tags'][entity_index]
                        print(json.dumps(out))
                        entity_index = entity_index + 1
                slen = slen + len(tb['tokens'][i]) + 1
                i = i + 1


def dowork(args):
    read_textblocks(args.file[0])
    read_sentences(args.file[1])

parser = ArgumentParser(description='Parse textblock jsonl files and combine them using the tagged words to generate named-entity based jsonl')
parser.add_argument('file', nargs=2, help='textblock jsonl & tagged sentence jsonl')
args = parser.parse_args()
dowork(args)
