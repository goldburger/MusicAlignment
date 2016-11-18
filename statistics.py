import matplotlib.pyplot as plt
from data import *

#notes = read_maps('MAPS_ISOL_CH0.1_F_ENSTDkCL.txt')
notes = read_midi('song.mid')
onsets = onset_seq(notes)

distribution = np.zeros((88,))

for note in onsets:
    index = note_to_index[note[:-1]]+12*int(note[-1])
    distribution[index] += 1

plt.bar(range(88), distribution)
plt.show()
