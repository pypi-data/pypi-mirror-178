"""Console script for addthalesnumbers."""
import argparse
import sys
import addthalesnumbers as atn

def main():
    """Console script for addthalesnumbers."""
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()

    print("Thales Arguments: " + str(args._))
    return atn.addthalesnumbers.addnumbers(args)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
