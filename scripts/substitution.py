import matplotlib.pyplot as plt
import numpy as np

from data import *

def write_substitution_matrix(filename, S):
    notes = all_notes()

    with open(filename, 'w') as f:
        f.write('\t' + '\t'.join(notes) + '\n')
        for i, note in enumerate(notes):
            f.write('{0}\t{1}\n'.format(note, '\t'.join(list(map(str, S[i, :])))))

def gaussian(mu, s):
    return lambda x: 1. / (np.sqrt(2 * np.pi) * s) * \
        np.exp(-(x - mu) ** 2 / (2 * s ** 2))

def range_around(index):
    centered = np.zeros(88)
    for i in range(index+1, 88):
        centered[i] = i - index
    for i in range(0, index):
        centered[i] = index - i
    return centered

if __name__ == '__main__':
    distribution = np.atleast_2d(np.loadtxt('distribution.csv'))
    M, S = np.zeros((88, 88)), np.zeros((88, 88))

    for i in range(88):
        M[:, i] = gaussian(0, 2)(range_around(i))
        S[:, i] = np.log(M[:, i] / distribution[0, i])

    S = S.astype('int32')
    S[S<-10] = -10
    
    write_substitution_matrix('gaussian.txt', S)
    write_substitution_matrix('identity.txt', np.identity(88, dtype='int32'))
