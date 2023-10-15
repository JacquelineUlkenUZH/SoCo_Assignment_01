import argparse
import os
import time
from string import ascii_letters, digits, punctuation, whitespace, printable
from random import choice
import file_manager as fm

# Configuration variables
testprefix = "test_"
characterset = printable
testfile_directory = "testfiles/"
testfile_empty = testfile_directory + "testfile_empty.txt"
testfile_small = testfile_directory + "testfile_small.txt"
testfile_large = testfile_directory + "testfile_large.txt"
testfile_nonexistent = "thisfilenamedoesnotexist"

def setup(testcontent, function_name):
    """
    Create directory of name stored in global variable "testfile_directory".
    Create three files in that directory using global variables "testfile_empty", 
    "testfile_small", "testfile_large" and dictionary "testcontent".
    """
    try:
        if not os.path.exists(testfile_directory):
            os.makedirs(testfile_directory)
        with open(testfile_empty, "w"):
            pass
        with open(testfile_small, "w") as f:
            f.write(testcontent["small"])
        with open(testfile_large, "w") as f:
            f.write(testcontent["large"])
    except Exception as e:
        print(f"Setup for {function_name} failed with error {e}!")

def teardown(function_name):
    """Deletes all file in directory of name stored in global variable 
       "testfile_directory" and finally delete that directory.
    """
    for testfile in os.listdir(testfile_directory):
        try:
            os.remove(testfile_directory + testfile)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Teardown of {testfile} in {function_name} failed with error {e}!")

    os.rmdir(testfile_directory)

def get_random_string(length):
    """
    Random string using global variable "characterset" of length "length".
    """
    return ''.join(choice(characterset) for i in range(int(length)))


# Actual test functions
def test_create_file_empty(testcontent):
    empty_file = testfile_directory + "empty_file"
    success = fm.create_file(empty_file)
    with open(empty_file, "r") as file:
        content_matches = file.read() == ""

    actual = content_matches and success
    expected = True
    assert actual == expected


def test_create_file_with_content(testcontent):
    content = "content"
    with_content_file = testfile_directory + "with_content_file"
    success = fm.create_file(with_content_file, content)
    with open(with_content_file, "r") as file:
        content_matches = file.read() == content

    actual = content_matches and success
    expected = True
    assert actual == expected


def test_create_file_no_name(testcontent):
    no_name_file = ""
    actual = fm.create_file(no_name_file)
    expected = False
    assert actual == expected


def test_create_file_already_exists(testcontent):
    actual = fm.create_file(testfile_small, "content")
    expected = False
    assert actual == expected

def test_read_file_content_nonexistent(testcontent):
    actual = fm.read_file(testfile_nonexistent)
    expected = None
    assert actual == expected

def test_read_file_content_empty_correct(testcontent):
    actual = fm.read_file(testfile_empty)
    expected = ""
    assert actual == expected

def test_read_file_content_small_correct(testcontent):
    actual = fm.read_file(testfile_small)
    expected = testcontent["small"]
    assert actual == expected


def test_read_file_content_large_correct(testcontent):
    actual = fm.read_file(testfile_large)
    expected = testcontent["large"]
    assert actual == expected


def test_delete_file_small_correct(testcontent):
    actual = fm.delete_file(testfile_small)
    expected = True
    assert actual == expected


def test_delete_file_large_correct(testcontent):
    actual = fm.delete_file(testfile_large)
    expected = True
    assert actual == expected


def test_delete_file_empty(testcontent):
    actual = fm.delete_file(testfile_empty)
    expected = True
    assert actual == expected


def test_delete_file_not_found(testcontent):
    actual = fm.delete_file(testfile_nonexistent)
    expected = False
    assert actual == expected


def test_delete_file_while_open(testcontent):
    with open(testfile_small, "r") as file:
        actual = fm.delete_file(testfile_small)
        expected = False
        assert actual == expected and os.path.exists(testfile_small)


def test_cause_fail(testcontent):
    assert 1 == 2


def test_cause_error(testcontent):
    assert 1 / 0 == 2


def main():

    # Book-keeping variables to inform user at end
    funcnames_fail = []
    funcnames_error = []
    results = {"pass": 0, "fail": 0, "error": 0}

    # Helper variables for printing
    str_pass = "\033[92m" + "pass" + "\033[0m"
    str_fail = "\033[93m" + "fail" + "\033[0m"
    str_error = "\033[91m" + "error" + "\033[0m"
    
    # Test dictionary to hold content and in the future maybe more
    testcontent = {}
    testcontent["small"] = get_random_string(10e2)
    testcontent["large"] = get_random_string(10e5)

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--select", help="Select the tests to run with a keyword")
    args = parser.parse_args()
    
    print()

    for name, func in globals().items():
        if name.startswith(testprefix) and callable(func):
            if not args.select or args.select in name:
                setup(testcontent, name)
                start = time.time()
                try:
                    func(testcontent)
                    print(f"{str_pass:<15}", end="")
                    results["pass"] += 1
                except AssertionError:
                    msecs = (time.time() - start) * 1000
                    print(f"{str_fail:<15}", end="")
                    results["fail"] += 1
                    funcnames_fail.append(name)
                except Exception:
                    msecs = (time.time() - start) * 1000
                    print(f"{str_error:<15}", end="")
                    results["error"] += 1
                    funcnames_error.append(name)
                    
                msecs = (time.time() - start) * 1000
                print(f"{msecs:.1f}ms <- {name}")
                teardown(name)
    
    print("\n\nTest summary:\n-------------")
    print(f"\n{str_pass} {results['pass']}")
    print(f"\n{str_fail} {results['fail']}")
    for fail in funcnames_fail: print(fail)
    print(f"\n{str_error} {results['error']}")
    for error in funcnames_error: print(error)
    print()


if __name__ == "__main__":
    main()
