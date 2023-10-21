# SoCo_Assignment_01
Assignment 01 for the course Software Construction 23HS 22BI0004

1. We decided to look and study the assignment in the first week from October 4th until October 11th and then split the
   work between the three of us.
2. To do that, we met on October 11th after the lecture and lab and discussed the assignment. We thought about some test
   ideas for each function: ![img.png](img.png) We wrote down every idea that came to mind. There were some obvious ones
   such as testing if a file was created succesfully but also tests such as deleting a file that is currently open.
3. We then split the work in three parts:
    - Marc: writing teardown and setup and the dictionary, writing tests for read_file
    - Jackie: writing tests for create_file and write_file
    - Anna: writing tests for delete_file and writing readme.md
   # should I include why we split the assignment like this? (Marc willingly doing more because he has more time)
4. We created a discord group chat to organize, ask questions and coordinate.
5. We took the code from the lecture as our base and wrote the tests according to the lecture.
   # insert documentation of Marc and Jackie's part
6. We studied the file_manager.py file first to know exactly how the functions work and what they return.
7. Most of the tests have simple style in which we assert if the expected return value is the same as the actual.
8. For test_delete_file_while_open we first thought about checking if a file is already opened and then trying to delete
   it. But we were not sure how to do it. Another idea was to open a file and then trying to delete it. We did it like
   this.