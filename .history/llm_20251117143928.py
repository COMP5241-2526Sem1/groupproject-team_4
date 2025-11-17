import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv() # Loads environment variables from .env
# token = os.environ.get("GITHUB_TOKEN")
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-mini"

# A function to call an LLM model and return the response
def call_llm_model(model, messages, temperature=1.0, top_p=1.0):
	token = os.environ.get("GITHUB_TOKEN")
	client = OpenAI(base_url=endpoint, api_key=token)
	response = client.chat.completions.create(
		messages=messages,
		temperature=temperature, top_p=top_p, model=model
	)
	return response.choices[0].message.content


def generate_quiz_content(topic, teaching_materials="", num_questions=5):
	"""Generate quiz questions based on topic and teaching materials"""
	prompt = f"""Based on the topic: "{topic}", create a quiz with {num_questions} questions.

Teaching materials/context:
{teaching_materials if teaching_materials else "Generate based on the topic"}

Create a JSON response with this structure:
{{
    "quiz_name": "Quiz name",
    "description": "Brief description",
    "duration": 30,
    "questions": [
        {{
            "type": "mcq",
            "content": "Question text",
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
            "content": "Short answer question",
            "points": 3,
            "sample_answer": "Expected answer"
        }}
    ]
}}

Requirements:
- Mix MCQ and short answer questions
- University level difficulty
- Clear, unambiguous questions
- Accurate correct answers
- Vary point values (1-5 points)
- IMPORTANT: Return ONLY valid JSON, no extra text or explanations
"""
	
	messages = [
		{"role": "system", "content": "You are an expert educational content creator. Always respond with valid JSON only. Do not include any text before or after the JSON."},
		{"role": "user", "content": prompt}
	]
	
	try:
		response = call_llm_model(model, messages, temperature=0.7)
		# Try to clean the response if it contains extra text
		response = response.strip()
		
		# If the response starts with ```json, extract the JSON part
		if response.startswith("```json"):
			start = response.find("{")
			end = response.rfind("}") + 1
			if start != -1 and end != -1:
				response = response[start:end]
		elif response.startswith("```"):
			start = response.find("{")
			end = response.rfind("}") + 1
			if start != -1 and end != -1:
				response = response[start:end]
		
		return json.loads(response)
	except json.JSONDecodeError as e:
		print(f"JSON decode error: {e}")
		print(f"Raw response: {response}")
		# Return a fallback response
		return {
			"quiz_name": f"Quiz on {topic}",
			"description": f"Auto-generated quiz on {topic}",
			"duration": 30,
			"questions": [
				{
					"type": "mcq",
					"content": f"What is the main concept in {topic}?",
					"points": 2,
					"choices": [
						{"text": "Option A", "correct": true},
						{"text": "Option B", "correct": false},
						{"text": "Option C", "correct": false},
						{"text": "Option D", "correct": false}
					]
				}
			]
		}
	except Exception as e:
		print(f"Error generating quiz content: {e}")
		raise


def generate_poll_content(topic, teaching_materials="", num_questions=3):
	"""Generate poll questions for class engagement"""
	prompt = f"""Create a poll for class engagement on topic: "{topic}"

Teaching materials/context:
{teaching_materials if teaching_materials else "Generate based on the topic"}

Create a JSON response with this structure:
{{
    "poll_name": "Poll name",
    "description": "Brief description",
    "duration": 10,
    "questions": [
        {{
            "type": "mcq",
            "content": "Poll question text",
            "points": 0,
            "choices": [
                {{"text": "Option A", "correct": false}},
                {{"text": "Option B", "correct": false}},
                {{"text": "Option C", "correct": false}},
                {{"text": "Option D", "correct": false}}
            ]
        }}
    ]
}}

Requirements:
- Create {num_questions} questions
- Polls are for opinion/engagement (no correct answers)
- Set correct: false for all choices
- Set points: 0 for all questions
- Make questions thought-provoking
- Encourage class discussion
"""
	
	messages = [
		{"role": "system", "content": "You are an expert at creating engaging classroom polls. Always respond with valid JSON only."},
		{"role": "user", "content": prompt}
	]
	
	response = call_llm_model(model, messages, temperature=0.8)
	return json.loads(response)


def generate_short_answer_content(topic, teaching_materials="", num_questions=3):
	"""Generate short answer questions"""
	prompt = f"""Create short answer questions on topic: "{topic}"

Teaching materials/context:
{teaching_materials if teaching_materials else "Generate based on the topic"}

Create a JSON response with this structure:
{{
    "name": "Short Answer Activity name",
    "description": "Brief description",
    "duration": 20,
    "questions": [
        {{
            "type": "saq",
            "content": "Question text requiring detailed answer",
            "points": 5,
            "sample_answer": "Comprehensive sample answer",
            "grading_criteria": "Key points to look for in student answers"
        }}
    ]
}}

Requirements:
- Create {num_questions} questions
- Questions should require thoughtful, detailed answers
- Provide comprehensive sample answers
- Include grading criteria for each question
- Points: 3-10 per question
- Focus on critical thinking and analysis
"""
	
	messages = [
		{"role": "system", "content": "You are an expert at creating thought-provoking short answer questions. Always respond with valid JSON only."},
		{"role": "user", "content": prompt}
	]
	
	response = call_llm_model(model, messages, temperature=0.7)
	return json.loads(response)


def group_similar_answers(answers):
	"""Group similar student answers using AI"""
	if not answers or len(answers) < 2:
		return [{"group_id": 1, "answers": answers, "summary": "All answers"}]
	
	answers_text = "\n".join([f"{i+1}. {ans}" for i, ans in enumerate(answers)])
	
	prompt = f"""Analyze these student answers and group similar ones together.

Student answers:
{answers_text}

Create a JSON response with this structure:
{{
    "groups": [
        {{
            "group_id": 1,
            "theme": "Main theme or concept in this group",
            "answer_indices": [1, 3, 5],
            "summary": "Summary of common points in this group"
        }}
    ]
}}

Requirements:
- Group answers with similar concepts/themes
- Each answer should be in exactly one group
- Provide a clear theme for each group
- Include summary of key points
- Use answer indices (1-based) from the list above
"""
	
	messages = [
		{"role": "system", "content": "You are an expert at analyzing and categorizing text responses. Always respond with valid JSON only."},
		{"role": "user", "content": prompt}
	]
	
	response = call_llm_model(model, messages, temperature=0.5)
	result = json.loads(response)
	
	# Format result to include actual answers
	grouped_answers = []
	for group in result.get('groups', []):
		indices = group.get('answer_indices', [])
		group_answers = [answers[i-1] for i in indices if 0 < i <= len(answers)]
		grouped_answers.append({
			"group_id": group.get('group_id'),
			"theme": group.get('theme'),
			"answers": group_answers,
			"summary": group.get('summary')
		})
	
	return grouped_answers