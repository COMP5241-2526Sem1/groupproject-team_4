from app import app
from models.poll import Poll
from models.course import Course

with app.app_context():
    # Get all polls
    polls = Poll.query.all()
    print(f"Total polls in database: {len(polls)}\n")
    
    for poll in polls:
        course = Course.query.get(poll.course_code)
        course_name = course.name if course else "Unknown"
        print(f"Poll ID: {poll.id}")
        print(f"  Course: {poll.course_code} ({course_name})")
        print(f"  Name: {poll.name}")
        print(f"  Questions: {len(poll.questions)}")
        print()
