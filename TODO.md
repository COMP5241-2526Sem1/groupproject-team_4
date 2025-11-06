# TO-DO LIST
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