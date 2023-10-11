import argparse

# Configuration variables
testfile_empty = "testfile_empty.txt"
testfile_small = "testfile_small.txt"
testfile_large = "testfile_large.txt"
testprefix = "test_"



# Handling arguments
parser = argparse.ArgumentParser()
parser.add_argument("--select", help="Select the tests to run with a keyword")
args = parser.parse_args()


# Our helper functions
def setup(contentsmall, contentlarge):
    pass

def teardown():
    pass


def test_printing():
    print("Printing this")

def test_flexibility():
    print("very flexible")


def main():
    for name, fnc in globals().items():
        if name.startswith(testprefix):
            if ( args.select and args.select in name ) or not args.select:
                setup()
                fnc()
                teardown()

if __name__ == "__main__":
    main()

