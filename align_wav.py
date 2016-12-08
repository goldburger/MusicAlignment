import argparse
import os

from scripts.data import read_midi, poly_onset_seq, output_csv, read_wav
from scripts.to_json import csv_to_json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--wav', dest='wav', required=True)
    parser.add_argument('-m', '--mid', dest='mid', required=True)
    args = parser.parse_args()

    read_wav(args.wav, 'temp.mid')
    seq1 = poly_onset_seq(read_midi('temp.mid'))
    seq2 = poly_onset_seq(read_midi(args.mid))

    output_csv(seq1, 'data/fasta/seq1.csv')
    output_csv(seq2, 'data/fasta/seq2.csv')

    os.system('java MusicAlign data/fasta/seq1.csv data/fasta/seq2.csv matrices/gaussian.txt 2 1 -p')
    os.system('tail -r x.csv > data/fasta/x.csv')
    os.system('tail -r y.csv > data/fasta/y.csv')

    with open('visualizations/output.json', 'w') as f:
        f.write(csv_to_json('data/fasta/x.csv', 'data/fasta/y.csv'))

    os.system('rm x.csv y.csv')
