from app import app
from models.poll import Poll
from models.question import Question
from models.choice import Choice
from database import db
from datetime import datetime, timedelta

with app.app_context():
    # Create a poll for PHYS101
    poll = Poll(
        course_code='PHYS101',
        name='Physics Understanding Poll',
        description='Test your understanding of key physics concepts',
        created_by=3,  # david_chen is user_id 3
        created_at=datetime.now(),
        start_datetime=datetime.now() - timedelta(days=1),
        end_datetime=datetime.now() + timedelta(days=10),
        duration=20,
        attempt_limit=2,
        point=0,
        point_in_course=0,
        after_submitted_question_visible=True,
        after_submitted_student_response_visible=True,
        after_submitted_sample_response_visible=True,
        after_submitted_class_response_visible=True
    )
    db.session.add(poll)
    db.session.flush()  # Flush to get the poll ID
    
    poll_id = poll.id
    print(f"Created poll with ID: {poll_id}")
    
    # Create 3 questions
    questions_data = [
        '物理学中力的基本定义是什么？',
        '能量守恒定律指出什么？',
        '热力学第二定律在日常生活中的应用是什么？'
    ]
    
    questions = []
    for q_text in questions_data:
        q = Question(
            poll_id=poll_id,
            type='mcq',
            content=q_text,
            points=0
        )
        db.session.add(q)
        db.session.flush()
        questions.append(q)
    
    # Create choices for each question
    choices_data = [
        [  # Question 1
            ('物体在单位时间内的质量变化', False),
            ('单位质量受到的加速度', False),
            ('作用在物体上，使其改变运动状态的原因', True),
            ('物体克服摩擦力所做的功', False),
        ],
        [  # Question 2
            ('能量可以被创造和销毁', False),
            ('能量既不能创造也不能销毁，只能转换', True),
            ('能量总是减少的', False),
            ('能量总是增加的', False),
        ],
        [  # Question 3
            ('冰箱制冷保持食物新鲜', True),
            ('热水自动冷却到室温', True),
            ('电灯发光发热', False),
            ('水从高处流向低处', False),
        ]
    ]
    
    for i, question in enumerate(questions):
        for choice_text, is_correct in choices_data[i]:
            c = Choice(
                question_id=question.id,
                content=choice_text,
                is_correct=is_correct
            )
            db.session.add(c)
    
    db.session.commit()
    print("✓ Poll with 3 questions and 12 choices created successfully!")
    print(f"Poll ID: {poll_id}")
    
    # Verify
    poll_check = Poll.query.get(poll_id)
    questions_check = Question.query.filter_by(poll_id=poll_id).all()
    print(f"Verified: Poll '{poll_check.name}' has {len(questions_check)} questions")
