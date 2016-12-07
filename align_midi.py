import argparse
import os

from scripts.data import read_midi, onset_seq, output_fasta
from scripts.to_json import to_json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seq1', dest='seq1', required=True)
    parser.add_argument('--seq2', dest='seq2', required=True)
    parser.add_argument('--mat', dest='mat', required=True)
    args = parser.parse_args()

    seq1 = onset_seq(read_midi(args.seq1))
    seq2 = onset_seq(read_midi(args.seq2))

    output_fasta(seq1, 'seq1', 'data/fasta/seq1.fasta')
    output_fasta(seq2, 'seq2', 'data/fasta/seq2.fasta')

    os.system('java MusicAlign data/fasta/seq1.fasta data/fasta/seq2.fasta {0} 10 1 -g > {1}'.format(args.mat, 'visualizations/output.txt'))

    with open('visualizations/output.json', 'w') as f:
        f.write(to_json('visualizations/output.txt'))
