import matplotlib.pyplot as plt
import numpy as np

from data import *

def write_substitution_matrix(filename, S):
    notes = []
    for octave in range(8):
        for note in index_to_note:
            notes.append('{0}{1}'.format(note, octave))
    notes = notes[:-8]

    with open(filename, 'w') as f:
        f.write('\t' + '\t'.join(notes) + '\n')
        for i, note in enumerate(notes):
            f.write('{0}\t{1}\n'.format(note, '\t'.join(list(map(str, S[i, :])))))

if __name__ == '__main__':
    distribution = np.atleast_2d(np.loadtxt('distribution.csv'))
    M, S = np.zeros(88), np.zeros(88)

    #gaussian = lambda x, s, a: 1. / np.sqrt(2 * np.pi * s ** 2) * \
    #    np.exp(-(x - a) ** 2 / 2 * s ** 2)

    #for i in range(88):
    #    for j in range(88):
    #        M[i, j] = gaussian(i, 1, )

    #for i in range(88):
    #    S[:, j] = np.log(M[:, j] / distribution[j])

    S = np.identity(88, dtype='int32')
    #np.savetxt('substitution.txt', S, delimiter=' ', fmt='%i')
    write_substitution_matrix('substitution.txt', S)
