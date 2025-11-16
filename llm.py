import os
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