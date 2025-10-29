# TO-DO LIST
## authentication system
use cookie
used at every action

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
both poll and quiz go into submission
poll.id, quiz.id, student.id, update_time, mcq_answer(one or multiple), saq_answer, grade(if applicable)
word cloud: generate from saq, external package