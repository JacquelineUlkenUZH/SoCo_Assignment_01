# SoCo Assignment 01
Assignment 1 for the course Software Construction 23HS 22BI0004. 

`run_tests.py` is a custom testing framework for four functions in `file_manager.py` as provided in class: 
- `read_file(filename)`
- `create_file(file_name, content="")`
- `write_file(file_name, content)`
- `delete_file(file_name)`

Expected results were taken from the provided SoCo-assignment_01.pdf and the function descriptions in `run_tests.py`.

## Getting started
usage: run_tests.py \[-h\] \[--select SELECT\] \[--selftest\]

options:
  -h, --help       show this help message and exit
  --select SELECT  Select the tests to run with a keyword
  --selftest       Include selftests of the testing system

Command-line arguments are parsed using `argparse`.

## Main findings
- `create_file(...)` overwrites existing files, which we consider a failure, given the description that it creates a *new* file.
- `write_file(...)` creates a new file if given an non-existent filename, which we consider a failure, given the description that it writes to *existing* files (and would otherwise behave just like `create_file(...)`).
- Whitespaces cause failures because `create_file(...)`, `read_file(...)` and `write_file(...)` rely on the default behaviour of the `open(...)` function of Python, which is opinionated and alters carriage returns ("\\r") and newlines ("\\n").
## Overview of framework

This framework runs and catalogues a series of test functions.

1.) Before each run, random small, large and whitespace **strings are generated** and stored in a dictionary `testcontent` that we pass around. We used charactersets of the `string` library. Only the whitespace string contains whitespaces.
2.) Before each test, `setup()` creates a testing environment in a **test folder** containing an empty file as well as one test file for each of the three sample strings.
3.) Test functions with prefix "test_" are selected using **introspection**. If the user uses `--select`, the selection is further narrowed.
4.) Tests are timed using `time` and results are catalogued.
5.) After each test, `teardown()` **deletes the test folder**.
6.) If `--selftest` is specified, three additional self-tests of the testing are run.
7.) Results are printed. The names of failed tests and errors are summarized for convenience at the end.

## Description of Tests
### Testing the delete_file() function
For `test_delete_file_while_open()` we first thought about checking if a file is already opened with the `.closed()` function
and then trying to delete it. We tried to implement it this way but an unresolved attribute reference came up. In
addition, this implementation only checks if the file is closed and not if it actually can be deleted. To solve this, we
came up with the idea to open the file and then trying to delete it, and asserting if the return value is "False".

### Testing the read_file() function
`test_read_file_content_empty_correct()` reads our empty test file and expects an **empty string** to be returned. `test_read_file_content_nonexistent()` expects that attempting to read a non-existent file returns **`None`**.

`test_read_file_content_small_correct()` and `test_read_file_content_large_correct()` check if `read_file()` returns the **original strings** we saved in our dictionary `testcontent` and our test files. (Reminder: These exclude whitespaces.)

`test_read_file_with_whitespaces()` checks if `read_file()` reads the test file containing our random string with whitespaces and expects it to be equal to the original stored in our dictionary `testcontent`.
### Testing the create_file() function
The functions `test_create_file_empty()` and `test_create_file_with_content()` test the basic functionality of file 
creation by using the `create_file()` function to create an empty file and a file with content respectively. The 
`test_create_file_no_name()` tests what happens if an empty string is given as a file name. The expected behavior here 
is that the function should throw an exception. 

The docstring of `create_file()` states that the function should create a *new* file. Thus, an existing file shouldn't 
be overwritten or edited by this function. The `test_create_file_already_exists()` function tests this behavior. 

### Testing the write_file() function
The `write_file()` function is very similar to the `create_file()` function. Again we are testing basic functionality, 
by writing to an empty file and writing to a file with a lot of content. 

This time, the docstring of `write_file()` states that it should write content to an *existing* file. It should not 
create a new file. To test this, we implemented the `test_write_file_nonexistent()` function.

`test_write_file_with_whitespaces()` uses `write_file()` to overwrite our testfile containing whitespaces. It then reads the content back itself and compares it to the original string in `testcontent`. The test passes if both `write_file()` returns `True` and the file content remains the same.

## Organization
We decided to look and study the assignment in the first week from October 4th until October 11th. We thought about some test ideas for each function. We wrote down every idea that came to mind. 

We then split the work between the three of us. We also created a discord group chat to organize, ask questions and coordinate.