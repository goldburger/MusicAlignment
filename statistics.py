import matplotlib.pyplot as plt
from data import *

import glob

distribution = np.zeros((88,))

for f in glob.glob('data/midi/*.mid'):
    notes = read_midi(f)
    onsets = onset_seq(notes)

    for note in onsets:
        index = note_to_index(note)
        distribution[index] += 1

plt.bar(range(88), distribution)
plt.show()
