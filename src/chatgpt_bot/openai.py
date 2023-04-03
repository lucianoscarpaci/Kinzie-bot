from dotenv import load_dotenv
import openai
import os

load_dotenv()

openai.api_key = os.getenv('CHATGPT_API_KEY')

def chatgpt_response(prompt):
    # program needs to have prevention from a timeout to openAI
    retry_count = 0
    max_retries = 9999

    while retry_count <= max_retries:
        try:
            # call openai api
            response = openai.Completion.create(
                # model type
                model="text-davinci-003",
                prompt=prompt,
                temperature=1,
                max_tokens=4000,
            )
            
            response_dict = response.get("choices")
            if response_dict and len(response_dict) > 0:
                prompt_response = response_dict[0]["text"]
            return prompt_response
    
        except Exception:
            retry_count += 1

        