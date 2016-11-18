import matplotlib.pyplot as plt
import numpy as np
import math

from mido import MidiFile, tempo2bpm
from operator import itemgetter
from collections import namedtuple

Note = namedtuple('Note', ['onset', 'offset', 'index'])

index_to_note = {
    0: 'A',
    1: 'A#',
    2: 'B',
    3: 'C',
    4: 'C#',
    5: 'D',
    6: 'D#',
    7: 'E',
    8: 'F',
    9: 'F#',
    10: 'G',
    11: 'G#'
}

def r_int(num): return int(round(num))
def f_int(num): return int(math.floor(num))
def index_to_octave(index):
    note = index % 12
    octave = f_int(index/12)
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
    return ''.join(seq)

if __name__ == '__main__':
    notes = read_midi('song.mid')
    roll = piano_roll(notes, 0.05)
    plt.imshow(roll)
    plt.show()
