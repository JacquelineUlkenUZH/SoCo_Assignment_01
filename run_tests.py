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
str_position = f"\033[A\033[80C"
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
    pass


# Actual test functions
def test_create_file_empty():
    empty_file = testfile_directory + "empty_file"
    success = fm.create_file(empty_file)
    with open(empty_file, "r") as file:
        content_matches = file.read() == ""

    actual = content_matches and success
    expected = True
    assert actual == expected


def test_create_file_with_content():
    content = "content"
    with_content_file = testfile_directory + "with_content_file"
    success = fm.create_file(with_content_file, content)
    with open(with_content_file, "r") as file:
        content_matches = file.read() == content

    actual = content_matches and success
    expected = True
    assert actual == expected


def test_create_file_no_name():
    no_name_file = ""
    actual = fm.create_file(no_name_file)
    expected = False
    assert actual == expected


def test_create_file_already_exists():
    actual = fm.create_file(testfile_small, "content")
    expected = False
    assert actual == expected


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
    actual = fm.delete_file("asdf")
    expected = False
    assert actual == expected

def test_delete_file_already_opened():
    if testfile_small.closed == False:
        actual = fm.delete_file(testfile_small)
        expected = False
        assert actual == expected

def test_cause_fail():
    assert 1 == 2


def test_cause_error():
    assert 1 / 0 == 2


def main():
    print()  # newline
    fails = []
    errors = []
    for name, func in globals().items():
        if name.startswith(testprefix) and callable(func):
            if not args.select or args.select in name:
                setup(name)
                print(f"{name}")
                try:
                    func()
                    print(str_position, str_pass)
                    results["pass"] += 1
                except AssertionError:
                    print(str_position, str_fail)
                    results["fail"] += 1
                    fails.append(name)
                except Exception:
                    print(str_position, str_error)
                    results["error"] += 1
                    errors.append(name)
                teardown(name)
    print("\nTest summary:\n-------------")
    print(f"\n{str_pass} {results['pass']}")
    print(f"\n{str_fail} {results['fail']}")
    for fail in fails: print(fail)
    print(f"\n{str_error} {results['error']}")
    for error in errors: print(error)
    print()

if __name__ == "__main__":
    main()
