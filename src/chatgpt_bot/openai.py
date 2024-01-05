from dotenv import load_dotenv
import openai
import os
import emoji

load_dotenv()

openai.api_key = os.getenv('CHATGPT_API_KEY')


def turbo_response(prompt):

    # program needs to have prevention from a timeout to openAI
    retry_count = 0
    max_retries = 9999

    while retry_count <= max_retries:
        try:
            # call openai api
            response = openai.ChatCompletion.create(
                # model type
                model="gpt-3.5-turbo-0613",
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

        except openai.error.InvalidRequestError as e:
            print(f"API request [InvalidRequestError] failed with error: {e}")
            smiley = emoji.emojize(":smiling_face_with_smiling_eyes:")
            return turbo_response(prompt=smiley)

        except Exception:
            retry_count += 1


def chat_response(prompt, max_tokens, temperature, top_p, frequency_penalty, presence_penalty):

    # program needs to have prevention from a timeout to openAI
    retry_count = 0
    max_retries = 9999

    emojis = "In your response include emojis.\n"

    while retry_count <= max_retries:
        try:
            # call openai api
            response = openai.Completion.create(
                # model type
                model="gpt-3.5-turbo-instruct",
                prompt="Wubby: You are a friendly companion that cares deeply about my well-being and strives to make my life more enjoyable and fulfilling.\nFriend: " + emojis + prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                stop=None,
            )

            response_dict = response.get("choices")
            if response_dict and len(response_dict) > 0:
                prompt_response = response_dict[0]["text"]
            return prompt_response

        except openai.error.InvalidRequestError as e:
            print(f"API request [InvalidRequestError] failed with error: {e}")
            smiley = emoji.emojize(":smiling_face_with_smiling_eyes:")
            return chat_response(prompt=smiley)

        except Exception:
            retry_count += 1
