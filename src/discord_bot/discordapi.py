from dotenv import load_dotenv
import discord
import os
from src.chatgpt_bot.openai import chatgpt_response
load_dotenv()


discord_token = os.getenv('DISCORD_TOKEN')

class MyClient(discord.Client):
    async def on_ready(self):
        print("login successful, you are: ", self.user)
    
    async def on_message(self, message):
        print(message.content)
        if message.author == self.user:
            return
        command, own_message=None, None

        for text in ['/ai','/bot','/chatgpt']:
            if message.content.startswith(text):
                command=message.content.split(' ')[0]
                own_message=message.content.replace(text, '')
                print(command, own_message)

        if command == '/ai' or command == '/bae' or command == '/chatgpt':
            bot_response = chatgpt_response(prompt=own_message)
            await message.channel.send(f"Hey boo {message.author.mention}, {bot_response}")

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)


        

