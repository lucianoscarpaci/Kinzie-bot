from dotenv import load_dotenv
import openai
import os
import asyncio
import discord

load_dotenv()

openai.api_key = os.getenv('CHATGPT_API_KEY')
discord_token = os.getenv('DISCORD_TOKEN')


def chatgpt_response(prompt):
    retry_count = 0
    max_retries = 9999

    while retry_count <= max_retries:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
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
        
        except Exception:
            retry_count += 1

class MyClient(discord.Client):
    async def on_ready(self):
        print("login successful, you are: ", self.user)
    
    async def on_message(self, message):
        print(message.content)
        if message.author == self.user:
            return
        command, own_message=None, None

        for text in ['/g','/bae']:
            if message.content.startswith(text):
                command=message.content.split(' ')[0]
                own_message=message.content.replace(text, '')
                print(command, own_message)

        if command == '/g' or command == '/bae':
            bot_response = chatgpt_response(prompt=own_message)
            await message.channel.typing()
            await asyncio.sleep(2)
            await message.channel.send(f"Hey boo {message.author.mention}, {bot_response}")

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

if __name__ == '__main__':
    client.run(discord_token)


        


            





        