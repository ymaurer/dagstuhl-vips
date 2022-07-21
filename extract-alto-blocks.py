#!/usr/bin/python
from argparse import ArgumentParser
import xml.etree.ElementTree as ET
import json
import re
import os

ns = {'mix': 'http://www.loc.gov/mix/v20',
    'xlink': 'http://www.w3.org/1999/xlink',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'mods': 'http://www.loc.gov/mods/v3',
    'MARC': 'http://www.loc.gov/MARC21/slim',
    'odrl': 'http://www.w3.org/ns/odrl/2/',
    'mets': 'http://www.loc.gov/METS/'
}

nsa = {'alto': 'http://www.loc.gov/standards/alto/ns-v3#',
    'xlink':'http://www.w3.org/1999/xlink'}

def parse_alto(fname, issue, page):
    root = ET.parse(fname)
    p = root.find('.//alto:Page', nsa)
    pagedata = {'page' : page}
    pagedata['page_height'] = p.attrib['HEIGHT']
    pagedata['page_width'] = p.attrib['WIDTH']
    for tb in root.findall(".//alto:TextBlock", nsa):
        words = []
        coords = []
        blockid = tb.attrib['ID']
        for st in tb.findall(".//alto:String", nsa):
            words.append(st.attrib['CONTENT'])
            coords.append({'x':st.attrib['HPOS'],
                        'y':st.attrib['VPOS'],
                        'w':st.attrib['WIDTH'],
                        'h':st.attrib['HEIGHT']
            })
        art = {'id': issue['ARK'] + '/pages/' + str(page) + '/textblock/' + blockid, 'tokens': words, 'token_coords': coords}
        print(json.dumps(art | pagedata | issue))
    

def dowork(args):
    for f in args.file:
        root = ET.parse(f)
        m = {'ARK': root.find('.').attrib['OBJID']}
        ri = root.find('.//mods:recordIdentifier', ns)
        expr = re.search('newspaper\/([^\/]*)\/(\d\d\d\d-\d\d-\d\d)', ri.text)
        m['paperid'] = expr.group(1)
        m['date'] = expr.group(2)
        alto = []
        for c in root.findall(".//mets:fileGrp[@USE='Text']/mets:file/mets:FLocat", ns):
            alto.append(os.path.dirname(f) + '/' + re.match('file:\/\/\.\/(.*)$', c.attrib['{http://www.w3.org/1999/xlink}href']).group(1))
        m['numpages'] = len(alto)
        for i, fname in enumerate(alto):
            parse_alto(fname, m, i + 1)

parser = ArgumentParser(description='Parse METS/ALTO files and extract textblocks from ALTO with coordinates')
parser.add_argument('file', nargs='*', help='mets files')
args = parser.parse_args()
dowork(args)

