# TO-DO LIST
## 20251107 refactor
1.refactor course model and its usage, remove course id and use course code eg COMP1010, keep the department but it should not be int but code, eg COMP, and add a new field for the second part of the code, eg 1010
2.refactor the department model, remove department id and use department code eg COMP, keep other field unchanged
3.refactor the usage of deparment in other places, eg user model
4.refactor all usage of course id to course code, this might take some time, do it carefully
after this, make a git commit called refactor: refactor course and department model and usage
then do
1.implement the quiz visibility feature
    after_submitted_question_visible = Column(Boolean, default=False)
    after_submitted_student_response_visible = Column(Boolean, default=False)
    after_submitted_sample_response_visible = Column(Boolean, default=False)
    after_submitted_class_response_visible = Column(Boolean, default=False)
    update the route and template to use the new visibility settings
2.poll should be exactly the same as quiz except that it is not graded and is always visible to user for the user response history, question and class response, user can see how other students responded to the poll
this will take some time, update the route and template
3.after this, make a git commit called feat: implement poll visibility feature

then do
add feature, teacher can see all quiz and poll in a course, teacher can do quiz and poll without limit
teacher can create, modify, delete quiz and poll
this will take time, add or modify routes and templates for this feature
after this, make a git commit called feat: teacher edit quiz and poll
then 
refactor the course management for teacher
teacher can manage who join the course 
teacher can see all students in the database
teacher can add, remove, update student in the course
this will take time, add or modify routes and templates for this feature
study the existing code carefully
beautify the existing layout and css, show student in rows, check box should be on the right hand side




## general
password=comp5241
hashed=scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88

git commit
feat, fix, docs, style, refactor, test, chore

## authentication system
flask built-in

## course home
announcement

quiz: click, show all possible quiz (newest first)
route course/3/quiz get quiz list
click a quiz, show quiz info, attempt number, max attempt allowed, start button
start the quiz, show all questions(mcq or saq)
mcq have choices
saq have input box
click submit, arrange the answers in json, send to server
show submit success page, stop quiz, go back to quiz list


poll: click, show all possible poll (newest first)
similar to quiz

word cloud: click, show all possible word cloud (newest first)
mini games: click, show all possible minigames (newest first)
grads
## activity
### mcq and saq
#### multiple-choice-questions(mcq)
id, course.id, quiz.id, poll.id, question, choices(String, separated by ;), answer(String, separated by ;)

#### short-answer-questions(saq)
id, course.id, quiz.id, poll.id, question

### poll and quiz
#### poll
id, course.id, title

mcq, saq, Not graded, visability, access control

quiz: mcq, saq, graded, visability, attempt, access control
teacher create, edit, delete activity, POST, PUT, DELETE
student get and answer poll and quiz, GET, POST
teacher get response, GET

### submission
student respond to a task(eg. poll, quiz, word cloud or mini-game) by a submission
if the teacher want to grade a submission
the system will look up the quiz id(or other id of the task) in that submission
and then look up the answers to the quiz
word cloud: generate from saq, external package