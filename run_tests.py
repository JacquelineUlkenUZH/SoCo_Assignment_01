import argparse
import os
from file_manager import read_file, create_file, write_file, delete_file

# Configuration variables
testfile_empty = "testfile_empty.txt"
testfile_small = "testfile_small.txt"
testfile_large = "testfile_large.txt"
testfiles = [testfile_empty, testfile_small, testfile_large]
testcontent_small = 'This is testcontent with\na new line!'
testcontent_large = 'This is testcontent with\na new line!' * 1000
testprefix = "test_"



# Handling arguments
parser = argparse.ArgumentParser()
parser.add_argument("--select", help="Select the tests to run with a keyword")
args = parser.parse_args()


# Our helper functions
def setup(fnc_name):
    with open(testfile_empty, 'w') as f:
        pass
    with open(testfile_small, 'w') as f:
        f.write(testcontent_small)
    with open(testfile_large, 'w') as f:
        f.write(testcontent_large)

def teardown(fnc_name):
    for testfile in testfiles:
        try:
            os.remove(testfile)
        except FileNotFoundError:
            pass
        except Exception:
            print(f"Teardown of {testfile} in {fnc_name} failed!")



def test_printing():
    with open(testfile_small, "r") as f:
        print(f.read())

def test_flexibility():
    print("very flexible")


def main():
    for name, fnc in globals().items():
        if name.startswith(testprefix):
            if not args.select or args.select in name:
                setup(name)
                fnc()
                teardown(name)

if __name__ == "__main__":
    main()

# test