import argparse
import os
from file_manager import read_file, create_file, write_file, delete_file

# Configuration variables
testfile_empty = "testfile_empty.txt"
testfile_small = "testfile_small.txt"
testfile_large = "testfile_large.txt"
testfiles = [testfile_empty, testfile_small, testfile_large]
testcontent_small = "This is test content with\na new line!"
testcontent_large = "This is test content with\na new line!" * 1000
testprefix = "test_"

# Handling arguments
parser = argparse.ArgumentParser()
parser.add_argument("--select", help="Select the tests to run with a keyword")
args = parser.parse_args()


# Setup and teardown
def setup(fnc_name):
    with open(testfile_empty, "w"):
        pass
    with open(testfile_small, "w") as f:
        f.write(testcontent_small)
    with open(testfile_large, "w") as f:
        f.write(testcontent_large)


def teardown(function_name):
    for testfile in testfiles:
        try:
            os.remove(testfile)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Teardown of {testfile} in {function_name} failed with error {e}!")


# Tests
def test_printing():
    with open(testfile_small, "r") as f:
        print(f.read())


def test_flexibility():
    print("very flexible")


# Main
def main():
    for name, func in globals().items():
        if name.startswith(testprefix):
            if not args.select or args.select in name:
                setup(name)
                func()
                teardown(name)


if __name__ == "__main__":
    main()
