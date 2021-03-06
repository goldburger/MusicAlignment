import matplotlib.pyplot as plt
import numpy as np

from data import *

def write_substitution_matrix(filename, S):
    notes = all_notes()

    with open(filename, 'w') as f:
        f.write(' '.join(notes) + '\n')
        for i, note in enumerate(notes):
            f.write(' '.join(list(map(str, S[i, :]))) + '\n')

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
    distribution = np.atleast_2d(np.loadtxt('matrices/distribution.csv'))
    M, S = np.zeros((88, 88)), np.zeros((88, 88))

    for i in range(88):
        M[:, i] = gaussian(0, 10)(range_around(i))
        S[:, i] = np.log(M[:, i] / distribution[0, i])
        S[i, i] = max(1, S[i, i])
        exclude = [j for j in range(88) if j != i]
        S[exclude, i] = S[exclude, i] - S[min(i+3, 87), i]

    S[S<-10] = -10

    write_substitution_matrix('matrices/gaussian.txt', S)
    write_substitution_matrix('matrices/identity.txt', np.identity(88))
