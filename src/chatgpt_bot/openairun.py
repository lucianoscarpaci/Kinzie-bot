from dotenv import load_dotenv
import openai
import os

load_dotenv()

openai.api_key = os.getenv('CHATGPT_API_KEY')

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Explain functional programming"},
    ],
    temperature=1,
    max_tokens=4000,
)

response_dict = response.get("choices")
if response_dict and len(response_dict) > 0:
    prompt_response = response_dict[0]["message"]["content"]

print(prompt_response)
            





        