import argparse
import os
import time
from string import ascii_letters, digits, punctuation, whitespace
from random import choice
import file_manager as fm

abspath = os.path.dirname(os.path.abspath(__file__))
os.chdir(abspath)

# Global configuration variables
TESTFILE_DIR = abspath + "/testfiles/"
TESTFILE_EMPTY = TESTFILE_DIR + "testfile_empty.txt"
TESTFILE_WHITESPACE = TESTFILE_DIR + "testfile_ws.txt"
TESTFILE_SMALL = TESTFILE_DIR + "testfile_small.txt"
TESTFILE_LARGE = TESTFILE_DIR + "testfile_large.txt"
TESTFILE_NONEXISTENT = TESTFILE_DIR + "thisfilenamedoesnotexist"


def setup(testcontent, function_name):
    """
    Run before every test. Create directory for the test file, and create three test files.

    Args:
        testcontent (dict): Dictionary containing the content of the test files.
        function_name (str): The name of the current test function.
    """

    try:
        if not os.path.exists(TESTFILE_DIR):
            os.makedirs(TESTFILE_DIR)
        with open(TESTFILE_EMPTY, "w"):
            pass
        with open(TESTFILE_SMALL, "w", newline="") as f:
            f.write(testcontent["small"])
        with open(TESTFILE_LARGE, "w", newline="") as f:
            f.write(testcontent["large"])
        with open(TESTFILE_WHITESPACE, "w", newline="") as f:
            f.write(testcontent["whitespace"])
    except Exception as e:
        print(f"Setup for {function_name} failed with error {e}!")


def teardown(function_name):
    """
    Run after every test. Delete all files in the test file directory, and then delete the directory itself.

    Args:
        function_name (str): The name of the current test function.
    """

    for testfile in os.listdir(TESTFILE_DIR):
        try:
            os.remove(TESTFILE_DIR + testfile)
        except Exception as e:
            print(f"Teardown of {testfile} in {function_name} failed with error {e}!")

    os.rmdir(TESTFILE_DIR)


def get_random_string(charset, length):
    """
    Given a set of characters, generate a random string of a given length.

    Args:
        charset (str): A string containing all available characters to use
        length (int): The length of the random string
    """
    return ''.join(choice(charset) for i in range(length))


# Actual test functions
def test_create_file_empty(testcontent):
    empty_file = TESTFILE_DIR + "empty_file"
    success = fm.create_file(empty_file)
    with open(empty_file, "r") as file:
        content_matches = file.read() == ""

    actual = content_matches and success
    expected = True
    assert actual == expected


def test_create_file_with_content(testcontent):
    with_content_file = TESTFILE_DIR + "with_content_file"
    success = fm.create_file(with_content_file, testcontent["large"])
    with open(with_content_file, "r", newline="") as file:
        content_matches = file.read() == testcontent["large"]

    actual = content_matches and success
    expected = True
    assert actual == expected


def test_create_file_no_name(testcontent):
    no_name_file = ""
    actual = fm.create_file(no_name_file)
    expected = False
    assert actual == expected


def test_create_file_already_exists(testcontent):
    success = fm.create_file(TESTFILE_SMALL, testcontent["large"])
    with open(TESTFILE_SMALL, "r", newline="") as file:
        content_is_original = file.read() == testcontent["small"]
    actual = success and not content_is_original
    expected = False
    assert actual == expected


def test_write_file_nonexistent(testcontent):
    actual = fm.write_file(TESTFILE_NONEXISTENT, testcontent["large"])
    expected = False
    assert actual == expected


def test_write_file_empty(testcontent):
    success = fm.write_file(TESTFILE_EMPTY, "")
    with open(TESTFILE_EMPTY, "r") as file:
        content_matches = file.read() == ""
    actual = content_matches and success
    expected = True
    assert actual == expected


def test_write_file_with_large_content(testcontent):
    success = fm.write_file(TESTFILE_LARGE, testcontent["large"])
    with open(TESTFILE_LARGE, "r") as file:
        content_matches = file.read() == testcontent["large"]

    actual = content_matches and success
    expected = True
    assert actual == expected


def test_write_file_with_whitespaces(testcontent):
    success = fm.write_file(TESTFILE_WHITESPACE, testcontent["whitespace"])
    with open(TESTFILE_WHITESPACE, "r", newline="") as file:
        content_matches = file.read() == testcontent["whitespace"]

    actual = content_matches and success
    expected = True
    assert actual == expected


def test_read_file_content_nonexistent(testcontent):
    actual = fm.read_file(TESTFILE_NONEXISTENT)
    expected = None
    assert actual == expected


def test_read_file_content_empty_correct(testcontent):
    actual = fm.read_file(TESTFILE_EMPTY)
    expected = ""
    assert actual == expected


def test_read_file_content_small_correct(testcontent):
    actual = fm.read_file(TESTFILE_SMALL)
    expected = testcontent["small"]
    assert actual == expected


def test_read_file_content_large_correct(testcontent):
    actual = fm.read_file(TESTFILE_LARGE)
    expected = testcontent["large"]
    assert actual == expected


def test_read_file_with_whitespaces(testcontent):
    actual = fm.read_file(TESTFILE_WHITESPACE)
    expected = testcontent["whitespace"]
    assert actual == expected


def test_delete_file_small_correct(testcontent):
    actual = fm.delete_file(TESTFILE_SMALL)
    expected = True
    assert actual == expected


def test_delete_file_large_correct(testcontent):
    actual = fm.delete_file(TESTFILE_LARGE) and not os.path.exists(TESTFILE_LARGE)
    expected = True
    assert actual == expected


def test_delete_file_empty(testcontent):
    actual = fm.delete_file(TESTFILE_EMPTY) and not os.path.exists(TESTFILE_EMPTY)
    expected = True
    assert actual == expected


def test_delete_file_not_found(testcontent):
    actual = fm.delete_file(TESTFILE_NONEXISTENT)
    expected = False
    assert actual == expected


def test_delete_file_while_open(testcontent):
    with open(TESTFILE_SMALL, "r"):
        actual = fm.delete_file(TESTFILE_SMALL) and not os.path.exists(TESTFILE_SMALL)
        expected = False
        assert actual == expected


# Self-tests of the testing system
def selftest_write_whitespaces(testcontent):
    with open(TESTFILE_WHITESPACE, "w", newline="") as file:
        file.write(testcontent["whitespace"])
    with open(TESTFILE_WHITESPACE, "r", newline="") as file:
        actual = file.read() == testcontent["whitespace"]

    expected = True
    assert actual == expected


def selftest_read_whitespaces(testcontent):
    with open(TESTFILE_WHITESPACE, "r", newline="") as file:
        actual = file.read() == testcontent["whitespace"]

    expected = True
    assert actual == expected


def selftest_cause_fail(testcontent):
    assert 1 == 2


def selftest_cause_error(testcontent):
    assert 1 / 0 == 2


def run_tests(command_line_args, test_prefix, testcontent):
    """
    Run all tests with the given test prefix.

    Args:
        command_line_args (Namespace): Keywords to select which tests should be run.
        test_prefix (str): Prefix of function names considered tests.
    """

    # Bookkeeping variables to inform user at end
    funcnames_fail = []
    funcnames_error = []
    results = {"pass": 0, "fail": 0, "error": 0}

    # Helper variables for printing
    str_pass = "\033[92m" + "pass" + "\033[0m"
    str_fail = "\033[93m" + "fail" + "\033[0m"
    str_error = "\033[91m" + "error" + "\033[0m"

    for name, func in globals().items():
        if name.startswith(test_prefix) and callable(func):
            if not command_line_args.select or command_line_args.select in name:
                setup(testcontent, name)
                start = time.time()
                try:
                    func(testcontent)
                    print(f"{str_pass:<15}", end="")
                    results["pass"] += 1
                except AssertionError:
                    print(f"{str_fail:<15}", end="")
                    results["fail"] += 1
                    funcnames_fail.append(name)
                except Exception as e:
                    print(e)
                    print(f"{str_error:<15}", end="")
                    results["error"] += 1
                    funcnames_error.append(name)

                msecs = (time.time() - start) * 1000
                print(f"{msecs:.1f}ms <- {name}")
                print()
                teardown(name)

    # Print summary
    print("\n\n-------------")
    print("Test summary:")
    print(f"\n{str_pass} {results['pass']}")
    print(f"\n{str_fail} {results['fail']}")
    for fail in funcnames_fail: print(fail)
    print(f"\n{str_error} {results['error']}")
    for error in funcnames_error: print(error)
    print("\n\n-------------")
    print()


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(
        prog='run_tests.py',
        description='Tests the program file_manager.py provided in class.',
        epilog='')
    parser.add_argument("--select", help="Select the tests to run with a keyword")
    parser.add_argument("--selftest", action='store_true', help="Include selftests of testing system")
    args = parser.parse_args()

    # Test dictionary to hold content and in the future maybe more
    CHARACTER_SET = ascii_letters + digits + punctuation
    testcontent = {"small": get_random_string(CHARACTER_SET, int(10e2)),
                   "large": get_random_string(CHARACTER_SET, int(10e5)),
                   "whitespace": get_random_string(CHARACTER_SET + whitespace, int(10e3))}

    run_tests(args, "test_", testcontent)
    if args.selftest:
        run_tests(args, "selftest_", testcontent)


if __name__ == "__main__":
    main()
