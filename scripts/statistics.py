import matplotlib.pyplot as plt
import numpy as np
import glob
import os

from data import *

distribution = np.zeros((88,))

for f in glob.glob('data/midi/*.mid'):
    try:
        notes = read_midi(f)
        onsets = onset_seq(notes)
    except:
        print("Removing: {0} - not a MIDI file".format(f))
        os.remove(f)
        continue

    for note in onsets:
        try:
            index = note_to_index(note)
            distribution[index] += 1
        except:
            print("Removing: {0} - out of piano range".format(f))
            os.remove(f)
            break

plt.bar(range(88), distribution / np.sum(distribution))
plt.show()
