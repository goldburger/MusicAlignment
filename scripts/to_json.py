from data import note_to_index

import argparse
import json
import re

starters = re.compile(r'[A-G\-]')
stoppers = re.compile(r'[0-9\-\_]')

def remove_dashes(n):
    if n[0] == '-':
        return n[0]
    return n

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', dest='input', required=True)
    parser.add_argument('--output', '-o', dest='output', required=True)
    args = parser.parse_args()

    seq1 = []
    seq2 = []

    with open(args.input, 'r') as f:
        _, a1, a2 = f.read().strip().split()
        note1, note2 = '', ''
        for i in range(len(a1.rstrip())):
            if a1[i] != '_':
                note1 += a1[i]
            if a2[i] != '_':
                note2 += a2[i]
            if stoppers.match(a1[i]) and stoppers.match(a2[i]):
                note1, note2 = remove_dashes(note1), remove_dashes(note2)
                seq1.append(note1) ; seq2.append(note2)
                note1, note2 = '', ''

    with open(args.output, 'w') as f:
        f.write(json.dumps({'s1': seq1, 's2': seq2}))
