"""."""
import sys

from classes.das import Das

# root = '/Users/reisnobre/Projects/process.vision/'
root = '/home/reisnobre/vision/'

if __name__ == "__main__":
    temp_file = sys.argv[1]
    temp_file = root + 'tmp/' + temp_file
    # temp_file = 'tmp/' + 'DAS-PGMEI-112019.pdf'
    das = Das(temp_file)
    print("{}".format(das.parse()))
    sys.exit(0)
