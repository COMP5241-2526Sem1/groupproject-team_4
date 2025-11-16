from flask import Blueprint, request, jsonify, session
from llm import call_llm_model
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