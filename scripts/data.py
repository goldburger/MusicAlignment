import matplotlib.pyplot as plt
import numpy as np
import math
import re

from mido import MidiFile, tempo2bpm
from operator import itemgetter
from collections import namedtuple

Note = namedtuple('Note', ['onset', 'offset', 'index'])

index_to_note = [
    'C', 'C#', 'D', 'D#', 'E', 'F',
    'F#', 'G', 'G#', 'A', 'A#', 'B'
]

def note_to_index(note):
    note = re.sub('\-', '', note)

    note_dict = { n: i for i, n in enumerate(index_to_note) }
    for flat in [('Bb', 1), ('Db', 4), ('Eb', 6), ('Gb', 9), ('Ab', 11)]:
        note_dict[flat[0]] = flat[1]
    return note_dict[note[:-1]] + 12 * int(note[-1]) - 9

def all_notes():
    notes = []
    for octave in range(9):
        for note in index_to_note:
            notes.append('{0}{1}'.format(note, octave))
    return notes[9:-11]

def r_int(num): return int(round(num))
def f_int(num): return int(math.floor(num))
def index_to_octave(index):
    note = (index + 9) % 12
    octave = f_int((index + 9)/12)
    return index_to_note[note] + str(octave)

def read_maps(filename):
    notes = []
    with open(filename) as f:
        f.readline()
        for line in f:
            onset, offset, note = line.strip().split()
            notes.append(Note(float(onset), float(offset), int(note)-21))
    return notes

def read_midi(filename):
    notes = []
    current_time = 0.
    for msg in MidiFile(filename):
        if msg.type == 'note_on':
            notes.append(Note(current_time+msg.time, 0, int(msg.note)-21))
        if msg.type == 'note_off':
            for i, note in enumerate(reversed(notes)):
                if note.index != msg.note - 21:
                    continue
                notes[len(notes)-i-1] = Note(note.onset, current_time+msg.time, note.index)
                break
        current_time += msg.time
    return notes

def piano_roll(notes, split=.01):
    last = max(notes, key=itemgetter(1))
    roll = np.zeros((88, r_int(last.offset/split)))
    for note in notes:
        roll[note.index, r_int(note.onset/split):r_int(note.offset/split)] = 1.
    return roll

def string_seq(notes, split=.01):
    seq = []
    for note in notes:
        for _ in range(r_int(note.onset/split), r_int(note.offset/split)):
            seq.append(index_to_octave(note.index))
    return seq

def onset_seq(notes):
    seq = []
    for note in notes:
        seq.append(index_to_octave(note.index))
    return seq

def seq_to_string(seq):
    output, current_line = '', ''
    for note in seq:
        if len(current_line) + len(note) < 80:
            current_line += note
        else:
            output += current_line + '\n'
            current_line = note
    if len(current_line) not in [2, 3]:
        output += current_line
    return output


def plot_piano_roll(notes):
    roll = piano_roll(notes, 0.05)
    plt.imshow(roll)
    plt.show()

def output_fasta(seq, name, filename):
    with open(filename, 'w') as f:
        f.write('>{0}\n{1}'.format(name, seq_to_string(seq)))

if __name__ == '__main__':
    notes = read_midi('data/midi/williams01.mid')
    output_fasta(onset_seq(notes), 'hedwig', 'hedwig.fasta')
    #plot_piano_roll(notes)
    #print(string_seq(notes))
