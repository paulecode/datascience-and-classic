# This program takes a midi, quickly describes it and converts it to CSV

# Imports

import sys


def main(args):
    for filename in args:
        print(filename)


if __name__ == "__main__":
    main(sys.argv[1:])
