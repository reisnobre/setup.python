"""."""
import sys

from classes.das import Das

if __name__ == "__main__":
    temp_file = sys.argv[1]
    temp_file = '/home/reisnobre/vision/tmp/' + temp_file
    das = Das(temp_file)
    print("{}".format(das.parse()))
    sys.exit(0)
