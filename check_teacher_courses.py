from app import app, db
from models.user import User
from models.course import Course
from models.minigame import Minigame

with app.app_context():
    # Check what courses debug_teacher owns
    teacher = User.query.filter_by(username='debug_teacher').first()
    
    if teacher:
        print(f'debug_teacher ID: {teacher.id}')
        
        # Check what courses this teacher owns
        courses = Course.query.filter_by(teacher_id=teacher.id).all()
        print(f'Teacher courses: {[(c.code, c.name) for c in courses]}')
        
        # Check if PHYS101 exists and who owns it
        phys_course = Course.query.filter_by(code='PHYS101').first()
        if phys_course:
            print(f'PHYS101 details: code={phys_course.code}, name={phys_course.name}, teacher_id={phys_course.teacher_id}')
            
            # Check if mini game 9 exists in PHYS101
            mini_game = Minigame.query.filter_by(id=9, course_code='PHYS101').first()
            if mini_game:
                print(f'Mini game 9 in PHYS101: id={mini_game.id}, name={mini_game.name}')
            else:
                print('Mini game 9 not found in PHYS101')
                
                # Check what mini games exist in PHYS101
                phys_mini_games = Minigame.query.filter_by(course_code='PHYS101').all()
                print(f'All mini games in PHYS101: {[(m.id, m.name) for m in phys_mini_games]}')
        else:
            print('PHYS101 course not found')
    else:
        print('debug_teacher user not found')