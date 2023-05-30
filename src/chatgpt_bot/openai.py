from dotenv import load_dotenv
import openai
import os

load_dotenv()

openai.api_key = os.getenv('CHATGPT_API_KEY')

def turbo_response(prompt):
    
    try:
        # call openai api
        response = openai.ChatCompletion.create(
            # model type
            model="gpt-3.5-turbo-0301",
            messages=[
                {"role": "user", "content": prompt},
            ],
            temperature=1,
            max_tokens=4000,
        )

        response_dict = response.get("choices")
        if response_dict and len(response_dict) > 0:
            prompt_response = response_dict[0]["message"]["content"]
        return prompt_response

    except openai.error.Timeout as e:
        print(f"API request failed with error: {e}")
        pass

    except openai.error.APIError as e:
        print(f"API request failed with error: {e}")
        pass

    except openai.error.APIConnectionError as e:
        print(f"API request failed with error: {e}")
        pass

    except openai.error.InvalidRequestError as e:
        print(f"API request failed with error: {e}")
        pass

    except openai.error.AuthenticationError as e:
        print(f"API request failed with error: {e}")
        pass

    except openai.error.PermissionError as e:
        print(f"API request failed with error: {e}")
        pass

    except openai.error.RateLimitError as e:
        print(f"API request failed with error: {e}")
        pass

def chat_response(prompt):

    emojis = "In your response include emojis.\n"

    try:
        # call openai api
        response = openai.Completion.create(
            # model type
            model="text-davinci-003",
            prompt="You are a friendly companion that cares deeply about my well-being and strives to make my life more enjoyable and fulfilling.\nFriend: " + emojis + prompt,
            temperature=0.5,
            max_tokens=4000,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
            stop=None,
        )
        
        response_dict = response.get("choices")
        if response_dict and len(response_dict) > 0:
            prompt_response = response_dict[0]["text"]
        return prompt_response

    except openai.error.Timeout as e:
        print(f"API request [Timeout] failed with error: {e}")
        pass

    except openai.error.APIError as e:
        print(f"API request [APIError] failed with error: {e}")
        pass

    except openai.error.APIConnectionError as e:
        print(f"API request [APIConnectionError] failed with error: {e}")
        pass

    except openai.error.InvalidRequestError as e:
        print(f"API request [InvalidRequestError] failed with error: {e}")
        pass

    except openai.error.AuthenticationError as e:
        print(f"API request [AuthenticationError] failed with error: {e}")
        pass

    except openai.error.PermissionError as e:
        print(f"API request [PermissionError] failed with error: {e}")
        pass

    except openai.error.RateLimitError as e:
        print(f"API request [RateLimitError] failed with error: {e}")
        return chat_response(prompt="You are a friendly companion that cares deeply about my well-being and strives to make my life more enjoyable and fulfilling.\nFriend: " + emojis + prompt)