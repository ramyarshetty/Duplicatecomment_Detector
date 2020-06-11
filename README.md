# DuplicateCommentDetector
Problem Statement:
Create a web project which can fetch the MCQ saved in the databse by passing its question id from front end(web page), further this web page should have an option to post answers under it. These answeres should be stored in the database after passing through "Detect the DuplicateFilter", in case filter returns duplicate throw error message "Duplicate".


Database Structure:
Table-1 Quiz, with the following below columns.

1.qid

2.question

3.option a

4.option b

5.option c

6.option d


Table-2 Answers, with the following below columns.

1.answer_id

2.answers

3.qid
