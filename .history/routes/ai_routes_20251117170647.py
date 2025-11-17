from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from llm import call_llm_model, generate_quiz_content, generate_poll_content, generate_short_answer_content, group_similar_answers
from models.quiz import Quiz
from models.poll import Poll
from models.short_answer import ShortAnswer
from models.question import Question
from models.choice import Choice
from models.question_response import QuestionResponse
from models.submission import Submission
from database import db
import json

ai_bp = Blueprint('ai', __name__)

def generate_quiz_prompt(user_input):
    """Generate a comprehensive quiz prompt based on user input"""
    prompt = f"""Based on the following topic: "{user_input}", create a comprehensive quiz with the following structure:

Please generate a JSON response with this exact structure:
{{
    "quiz_name": "A suitable quiz name based on the topic",
    "description": "A brief description of the quiz",
    "duration": 30,
    "attempt_limit": 3,
    "point_in_course": 10,
    "questions": [
        {{
            "type": "mcq",
            "content": "Question text here",
            "points": 2,
            "choices": [
                {{"text": "Choice A", "correct": true}},
                {{"text": "Choice B", "correct": false}},
                {{"text": "Choice C", "correct": false}},
                {{"text": "Choice D", "correct": false}}
            ]
        }},
        {{
            "type": "saq",
            "content": "Short answer question text here",
            "points": 3,
            "expected_answer": "Expected answer here"
        }}
    ]
}}

Guidelines:
1. Create 3-5 questions per quiz
2. Mix multiple choice and short answer questions
3. Make questions appropriate for university level
4. Ensure questions are clear and unambiguous
5. Provide realistic but challenging content
6. Make sure correct answers are accurate
7. Vary the point values (1-5 points per question)

The topic is: {user_input}"""
    return prompt

@ai_bp.route('/api/ai/quiz', methods=['POST'])
def generate_quiz():
    """Generate quiz content using AI"""
    try:
        data = request.get_json()
        user_input = data.get('input', '')
        
        if not user_input:
            return jsonify({"error": "No input provided"}), 400
        
        # Generate the prompt
        prompt = generate_quiz_prompt(user_input)
        
        # Prepare messages for the LLM
        messages = [
            {"role": "system", "content": "You are a helpful assistant that creates educational quiz content. Always respond with valid JSON only."},
            {"role": "user", "content": prompt}
        ]
        
        # Call the LLM model
        response = call_llm_model("openai/gpt-4.1-mini", messages, temperature=0.7)
        
        # Parse the JSON response
        try:
            quiz_data = json.loads(response)
            return jsonify(quiz_data)
        except json.JSONDecodeError:
            # If response is not valid JSON, try to extract JSON from it
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                quiz_data = json.loads(json_match.group())
                return jsonify(quiz_data)
            else:
                return jsonify({
                    "error": "Failed to generate valid quiz data",
                    "raw_response": response
                }), 500
        
    except Exception as e:
        return jsonify({
            "error": f"Error generating quiz: {str(e)}"
        }), 500


@ai_bp.route('/api/ai/poll', methods=['POST'])
def generate_poll():
    """Generate poll content using AI"""
    try:
        data = request.get_json()
        print(f"Poll request data: {data}")  # Debug logging
        topic = data.get('topic', '').strip() if data else ''
        teaching_materials = data.get('teaching_materials', '').strip() if data else ''
        num_questions = data.get('num_questions', 3) if data else 3
        
        print(f"Topic: '{topic}', Teaching materials: '{teaching_materials}', Num questions: {num_questions}")  # Debug logging
        
        if not topic:
            return jsonify({"error": "Topic is required"}), 400
        
        result = generate_poll_content(topic, teaching_materials, num_questions)
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in generate_poll: {str(e)}")  # Debug logging
        return jsonify({"error": f"Error generating poll: {str(e)}"}), 500


@ai_bp.route('/api/ai/short-answer', methods=['POST'])
def generate_short_answer():
    """Generate short answer questions using AI"""
    try:
        data = request.get_json()
        topic = data.get('topic', '')
        teaching_materials = data.get('teaching_materials', '')
        num_questions = data.get('num_questions', 3)
        
        if not topic:
            return jsonify({"error": "Topic is required"}), 400
        
        result = generate_short_answer_content(topic, teaching_materials, num_questions)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Error generating short answer questions: {str(e)}"}), 500


@ai_bp.route('/api/ai/save-quiz', methods=['POST'])
def save_generated_quiz():
    """Save AI-generated quiz to database"""
    try:
        data = request.get_json()
        course_code = data.get('course_code')
        quiz_data = data.get('quiz_data')
        
        if not course_code or not quiz_data:
            return jsonify({"error": "Missing required data"}), 400
        
        if 'user_id' not in session:
            return jsonify({"error": "Not authenticated"}), 401
        
        # Create quiz
        quiz = Quiz(
            course_code=course_code,
            name=quiz_data.get('quiz_name'),
            description=quiz_data.get('description'),
            created_by=session['user_id'],
            duration=quiz_data.get('duration', 30),
            attempt_limit=quiz_data.get('attempt_limit', 3),
            point_in_course=quiz_data.get('point_in_course', 10)
        )
        db.session.add(quiz)
        db.session.flush()
        
        # Create questions
        for q_data in quiz_data.get('questions', []):
            question = Question(
                quiz_id=quiz.id,
                type=q_data.get('type'),
                content=q_data.get('content'),
                points=q_data.get('points', 1)
            )
            db.session.add(question)
            db.session.flush()
            
            # Create choices for MCQ
            if q_data.get('type') == 'mcq':
                for choice_data in q_data.get('choices', []):
                    choice = Choice(
                        question_id=question.id,
                        content=choice_data.get('text'),
                        is_correct=choice_data.get('correct', False)
                    )
                    db.session.add(choice)
        
        db.session.commit()
        return jsonify({"success": True, "quiz_id": quiz.id})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error saving quiz: {str(e)}"}), 500


@ai_bp.route('/api/ai/save-poll', methods=['POST'])
def save_generated_poll():
    """Save AI-generated poll to database"""
    try:
        data = request.get_json()
        course_code = data.get('course_code')
        poll_data = data.get('poll_data')
        
        if not course_code or not poll_data:
            return jsonify({"error": "Missing required data"}), 400
        
        if 'user_id' not in session:
            return jsonify({"error": "Not authenticated"}), 401
        
        # Create poll
        poll = Poll(
            course_code=course_code,
            name=poll_data.get('poll_name'),
            description=poll_data.get('description'),
            created_by=session['user_id'],
            duration=poll_data.get('duration', 10)
        )
        db.session.add(poll)
        db.session.flush()
        
        # Create questions
        for q_data in poll_data.get('questions', []):
            question = Question(
                poll_id=poll.id,
                type='mcq',
                content=q_data.get('content'),
                points=0
            )
            db.session.add(question)
            db.session.flush()
            
            # Create choices
            for choice_data in q_data.get('choices', []):
                choice = Choice(
                    question_id=question.id,
                    content=choice_data.get('text'),
                    is_correct=False
                )
                db.session.add(choice)
        
        db.session.commit()
        return jsonify({"success": True, "poll_id": poll.id})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error saving poll: {str(e)}"}), 500


@ai_bp.route('/api/ai/save-short-answer', methods=['POST'])
def save_generated_short_answer():
    """Save AI-generated short answer questions to database"""
    try:
        data = request.get_json()
        course_code = data.get('course_code')
        sa_data = data.get('short_answer_data')
        
        if not course_code or not sa_data:
            return jsonify({"error": "Missing required data"}), 400
        
        if 'user_id' not in session:
            return jsonify({"error": "Not authenticated"}), 401
        
        # Create short answer activity
        short_answer = ShortAnswer(
            course_code=course_code,
            name=sa_data.get('name'),
            description=sa_data.get('description'),
            created_by=session['user_id'],
            duration=sa_data.get('duration', 20)
        )
        db.session.add(short_answer)
        db.session.flush()
        
        # Create questions
        for q_data in sa_data.get('questions', []):
            question = Question(
                short_answer_id=short_answer.id,
                type='saq',
                content=q_data.get('content'),
                points=q_data.get('points', 5)
            )
            db.session.add(question)
        
        db.session.commit()
        return jsonify({"success": True, "short_answer_id": short_answer.id})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error saving short answer: {str(e)}"}), 500


@ai_bp.route('/api/ai/group-answers', methods=['POST'])
def group_answers():
    """Group similar student answers using AI"""
    try:
        data = request.get_json()
        question_id = data.get('question_id')
        
        if not question_id:
            return jsonify({"error": "Question ID is required"}), 400
        
        # Get all text answers for this question
        responses = QuestionResponse.query.filter_by(
            question_id=question_id
        ).filter(
            QuestionResponse.text_answer.isnot(None)
        ).all()
        
        if not responses:
            return jsonify({"groups": []})
        
        # Extract answer texts
        answers = [r.text_answer for r in responses if r.text_answer]
        
        # Group similar answers
        grouped = group_similar_answers(answers)
        
        return jsonify({"groups": grouped})
        
    except Exception as e:
        return jsonify({"error": f"Error grouping answers: {str(e)}"}), 500


@ai_bp.route('/teacher/ai-generate/<course_code>')
def ai_generate_page(course_code):
    """Page for AI content generation"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    from models.course import Course
    course = Course.query.filter_by(code=course_code).first_or_404()
    
    return render_template('teacher_ai_generate.html', course=course)


@ai_bp.route('/teacher/ai-review/<content_type>/<int:content_id>')
def ai_review_page(content_type, content_id):
    """Page for reviewing and editing AI-generated content"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    content = None
    if content_type == 'quiz':
        content = Quiz.query.get_or_404(content_id)
    elif content_type == 'poll':
        content = Poll.query.get_or_404(content_id)
    elif content_type == 'short-answer':
        content = ShortAnswer.query.get_or_404(content_id)
    else:
        return "Invalid content type", 404
    
    return render_template('teacher_ai_review.html', 
                         content=content, 
                         content_type=content_type)


@ai_bp.route('/teacher/answer-analysis/<content_type>/<int:content_id>')
def answer_analysis_page(content_type, content_id):
    """Page for analyzing student answers with AI grouping"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    content = None
    if content_type == 'quiz':
        content = Quiz.query.get_or_404(content_id)
    elif content_type == 'poll':
        content = Poll.query.get_or_404(content_id)
    elif content_type == 'short-answer':
        content = ShortAnswer.query.get_or_404(content_id)
    else:
        return "Invalid content type", 404
    
    # Get all questions with responses
    from models.submission import Submission
    for question in content.questions:
        question.responses = QuestionResponse.query.filter_by(
            question_id=question.id
        ).join(Submission).all()
        
        # For MCQ, calculate statistics
        if question.type == 'mcq':
            stats = calculate_mcq_stats(question)
            question.response_stats = stats
    
    return render_template('teacher_answer_analysis.html', 
                         content=content, 
                         content_type=content_type)


def calculate_mcq_stats(question):
    """Calculate statistics for MCQ responses"""
    from collections import Counter
    
    responses = QuestionResponse.query.filter_by(question_id=question.id).all()
    
    if not responses:
        return {
            'labels': [],
            'counts': [],
            'colors': [],
            'total': 0,
            'correct': 0,
            'correct_percentage': 0,
            'most_common': 'N/A'
        }
    
    # Count responses for each choice
    choice_counts = Counter()
    correct_count = 0
    
    for response in responses:
        if response.choice_id:
            choice = Choice.query.get(response.choice_id)
            if choice:
                choice_counts[choice.text] += 1
                if choice.correct:
                    correct_count += 1
    
    # Prepare chart data
    labels = []
    counts = []
    colors = []
    
    for choice in question.choices:
        labels.append(choice.text)
        count = choice_counts.get(choice.text, 0)
        counts.append(count)
        # Green for correct, blue for incorrect
        colors.append('rgba(75, 192, 192, 0.6)' if choice.correct else 'rgba(54, 162, 235, 0.6)')
    
    most_common = choice_counts.most_common(1)[0][0] if choice_counts else 'N/A'
    total = len(responses)
    correct_percentage = round((correct_count / total * 100) if total > 0 else 0, 1)
    
    return {
        'labels': labels,
        'counts': counts,
        'colors': colors,
        'total': total,
        'correct': correct_count,
        'correct_percentage': correct_percentage,
        'most_common': most_common
    }