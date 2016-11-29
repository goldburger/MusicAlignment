import argparse
import json
import copy
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
    seq = []

    with open(filename, 'r') as f:
        _, a1, a2 = f.read().strip().split()
        note1, note2 = '', ''
        seq_note = {}
        count = 0
        for i in range(len(a1.rstrip())):
            if a1[i] != '_':
                note1 += a1[i]
            if a2[i] != '_':
                note2 += a2[i]
            if stoppers.match(a1[i]) and stoppers.match(a2[i]):
                note1, note2 = remove_dashes(note1), remove_dashes(note2)
                seq_note['t'] = count
                seq_note['l'] = 1
                if note1 == note2:
                    seq_note['c'] = 'c'
                    seq_note['ix'] = to_js_index(note1)
                    seq_note['acc'] = accidentals(note1)
                    seq.append(seq_note)
                if note1 == '-' or (note1 != note2 and note2 != '-' and note1 != '-'):
                    seq_note['c'] = 'b'
                    seq_note['ix'] = to_js_index(note2)
                    seq_note['acc'] = accidentals(note2)
                    seq.append(seq_note)
                if note2 == '-' or (note1 != note2 and note2 != '-' and note1 != '-'):
                    seq_note2 = copy.deepcopy(seq_note)
                    seq_note2['c'] = 'i'
                    seq_note2['ix'] = to_js_index(note1)
                    seq_note2['acc'] = accidentals(note1)
                    seq.append(seq_note2)
                note1, note2 = '', ''
                seq_note = {}
                count += 1

    return json.dumps({'s': seq})
