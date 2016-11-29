import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest='input', required=True)
    parser.add_argument('-o', '--output', dest='output', required=True)
    args = parser.parse_args()

    pass
