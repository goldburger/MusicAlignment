import argparse
import json
import re

starters = re.compile(r'[A-G\-]')
stoppers = re.compile(r'[0-9\-\_]')

def remove_dashes(n):
    if n[0] == '-':
        return n[0]
    return n

notes = {
    'C': 0, 'D': 1, 'E': 2, 'F': 3, 'G': 4, 'A': 5, 'B': 6
}

def to_js_index(note):
    if note == '-':
        return None
    return int(note[-1]) * 7 + notes[note[0]]

def accidentals(note):
    if len(note) < 3:
        return None
    return note[1]

def to_json(filename):
    seq1 = []
    seq2 = []

    with open(filename, 'r') as f:
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

    seq1 = [{'ix': to_js_index(note), 'acc': accidentals(note)} for note in seq1]
    seq2 = [{'ix': to_js_index(note), 'acc': accidentals(note)} for note in seq2]

    return json.dumps({'s1': seq1, 's2': seq2})
