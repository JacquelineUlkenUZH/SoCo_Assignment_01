# SoCo_Assignment_01
Assignment 01 for the course Software Construction 23HS 22BI0004

`run_tests.py` is a custom testing framework for four functions in `file_manager.py` which was provided in class:
- `read_file(filename)`
- `create_file(file_name, content="")`
- `write_file(file_name, content)`
- `delete_file(file_name)`

Expected results were taken from the provided SoCo-assignment_01.pdf and the function descriptions in `run_tests.py`.

## Getting started
usage: run_tests.py [-h] [--select SELECT] [--selftest]

Tests the program file_manager.py provided in class.

options:
  -h, --help       show this help message and exit
  --select SELECT  Select the tests to run with a keyword
  --selftest       Include selftests of the testing system

## Main findings
- `create_file(...)` overwrites existing files, which we consider a failure, given the description that it creates a *new* file.
- `write_file(...)` creates a new file if given an non-existent filename, which we consider a failure, given the description that it writes to *existing* files (and would otherwise behave just like `create_file(...)`).
- Whitespaces cause failures because `create_file(...)`, `read_file(...)` and `write_file(...)` rely on the default behaviour of the `open(...)` function of Python, which is opinionated and alters carriage returns ("\\r") and newlines ("\\n").

## Explanation and decisions
We took the code from the lecture as our base and wrote the tests according to the lecture. First, we studied the
file_manager.py file to know exactly how the functions work and what they return. Most of the tests have simple style in
which we assert if the expected return value is the same as the actual. The reason why parameter "testcontent" appears
in every test is so that all tests can be called the same way.

### Description of Tests
#### Testing the delete_file() function
For `test_delete_file_while_open()` we first thought about checking if a file is already opened with the `.closed()` function
and then trying to delete it. We tried to implement it this way but an unresolved attribute reference came up. In
addition, this implementation only checks if the file is closed and not if it actually can be deleted. To solve this, we
came up with the idea to open the file and then trying to delete it, and asserting if the return value is "False".

#### Testing the read_file() function
<!--- insert special cases from Marc -->

#### Testing the create_file() function
The functions `test_create_file_empty()` and `test_create_file_with_content()` test the basic functionality of file 
creation by using the `create_file()` function to create an empty file and a file with content respectively. The 
`test_create_file_no_name()` tests what happens if an empty string is given as a file name. The expected behavior here 
is that the function should throw an exception. 

The docstring of `create_file()` states that the function should create a *new* file. Thus, an existing file shouldn't 
be overwritten or edited by this function. The `test_create_file_already_exists()` function tests this behavior. 

#### Testing the write_file() function
The `write_file()` function is very similar to the `create_file()` function. Again we are testing basic functionality, 
by writing to an empty file and writing to a file with a lot of content. 

<!--- insert description of test_write_file_with_whitespaces() --->

This time, the docstring of `write_file()` states that it should write content to an *existing* file. It should not 
create a new file. To test this, we implemented the `test_write_file_nonexistent()` function.

### Setup and teardown
We had several different ideas and implementations before our final solution:
   - To test the create_file function, we need to create files. These should be deleted in the teardown function, but
     how will the teardown function find them? We had the idea to manually add them to a list or teardown just deletes
     everything without knowing what was created. We have a testfiles folder where all the testing happens and teardown
     completely deletes that folder at the end.
<!--- add the other teardowns and setups -->

### Printing and time measurement
<!--- Marc's part -->

## Organization
We decided to look and study the assignment in the first week from October 4th until October 11th and then split the
work between the three of us. To do that, we met on October 11th after the lecture and lab and discussed the assignment.
We thought about some test ideas for each function. 
We wrote down every idea that came to mind. There were some obvious ones such as testing if a file was created
succesfully but also tests such as deleting a file that is currently open. We then split the work in three parts:
   - Marc Chéhab: writing teardown and setup and the dictionary, writing tests for read_file, printing and time measurement
   - Jacqueline Ulken: writing tests for create_file and write_file
   - Anna Pang: writing tests for delete_file and writing README.md
In the end, this plan was not 100% accurate and we ended up helping each other, editing each others parts and having
meetings every now and then to work on the code together. We also created a discord group chat to organize, ask
questions and coordinate.