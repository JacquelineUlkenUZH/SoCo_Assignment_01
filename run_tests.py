import argparse
import os
import file_manager as fm

# Helper variables
testfile_directory = "testfiles/"
testfile_empty = testfile_directory + "testfile_empty.txt"
testfile_small = testfile_directory + "testfile_small.txt"
testfile_large = testfile_directory + "testfile_large.txt"
testcontent_small = "This is test content with\na new line!"
testcontent_large = "This is test content with\na new line!" * 1000
testprefix = "test_"
results = {"pass": 0, "fail": 0, "error": 0}
str_pass = "\033[92m" + "pass" + "\033[0m"
str_fail = "\033[93m" + "fail" + "\033[0m"
str_error = "\033[91m" + "error" + "\033[0m"

# Handling arguments
parser = argparse.ArgumentParser()
parser.add_argument("--select", help="Select the tests to run with a keyword")
args = parser.parse_args()


# Setup and teardown
def setup(function_name):
    try:
        if not os.path.exists(testfile_directory):
            os.makedirs(testfile_directory)
        with open(testfile_empty, "w"):
            pass
        with open(testfile_small, "w") as f:
            f.write(testcontent_small)
        with open(testfile_large, "w") as f:
            f.write(testcontent_large)
    except Exception as e:
        print(f"Setup for {function_name} failed with error {e}!")


def teardown(function_name):
    for testfile in os.listdir(testfile_directory):
        try:
            os.remove(testfile_directory + testfile)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Teardown of {testfile} in {function_name} failed with error {e}!")

    os.rmdir(testfile_directory)


# Actual test functions
def test_create_file():
    pass


def test_read_file_content_small_correct():
    actual = fm.read_file(testfile_small)
    expected = testcontent_small
    assert actual == expected


def test_read_file_content_large_correct():
    actual = fm.read_file(testfile_large)
    expected = testcontent_large
    assert actual == expected


def test_delete_file_small_correct():
    actual = fm.delete_file(testfile_small)
    expected = True
    assert actual == expected

def test_delete_file_large_correct():
    actual = fm.delete_file(testfile_large)
    expected = True
    assert actual == expected

def test_delete_file_empty():
    actual = fm.delete_file(testfile_empty)
    expected = True
    assert actual == expected

def test_delete_file_not_found():
    assert fm.delete_file(asdf) == FileNotFoundError

def test_cause_fail():
    assert 1 == 2


def test_cause_error():
    assert 1 / 0 == 2


def main():
    print()  # newline
    for name, func in globals().items():
        if name.startswith(testprefix) and callable(func):
            if not args.select or args.select in name:
                setup(name)
                print(f"{name:<60}", end="")
                try:
                    func()
                    print(str_pass)
                    results["pass"] += 1
                except AssertionError:
                    print(str_fail)
                    results["fail"] += 1
                except Exception:
                    print(str_error)
                    results["error"] += 1
                teardown(name)
    print("\nTest summary:\n-------------")
    print(f"{str_pass} {results['pass']}")
    print(f"{str_fail} {results['fail']}")
    print(f"{str_error} {results['error']}")


if __name__ == "__main__":
    main()
