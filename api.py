import anthropic
from dotenv import load_dotenv
from openai import OpenAI
import os
import google.generativeai as genai

load_dotenv()

# Anthropic model
anthropic_client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
anthropic_model = "claude-3-5-haiku-latest"

# Gemini model
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
gemini_generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
gemini_model="gemini-1.5-flash"

# OpenAI model
openai_client = OpenAI()
openai_model = "gpt-4o-mini"

def ask_anthropic(prompt, model=anthropic_model):
  # Use the latest Claude 3.5 Sonnet model when testing.
  message = anthropic_client.messages.create(
    model='claude-3-5-sonnet-latest',
    max_tokens=1024,
    messages=[
      {'role': 'user', 'content': prompt}
    ]
  )
  return message.content[0].text

def ask_gemini(prompt, model=gemini_model):
  gemini_model = genai.GenerativeModel(
    model_name=model,
    generation_config=gemini_generation_config)
  response = gemini_model.generate_content(prompt)
  return response.text 

def ask_openai(prompt, model=openai_model):
  completion = openai_client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ]
  )
  return completion.choices[0].message.content
