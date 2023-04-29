from dotenv import load_dotenv
import discord
import os
import asyncio
import requests
import json
from src.chatgpt_bot.openai import chatgpt_response
load_dotenv()


discord_token = os.getenv('DISCORD_TOKEN')
giphy_token = os.getenv('GIPHY_URL')

class MyClient(discord.Client):
    async def on_ready(self):
        print("login successful, you are: ", self.user)
    
    async def get_memes():
        url = giphy_token
        giphy_response = requests.get(url)
        return json.loads(giphy_response.text)['data']['url']
    
    async def on_message(self, message):
        print(message.content)
        if message.author == self.user:
            return
        command, own_message=None, None

        for text in ['Kinzie', 'kinzie']:
            if message.content.startswith(text):
                command=message.content.split(' ')[0]
                own_message=message.content.replace(text, '')
                print(command, own_message)

        if command == 'Kinzie' or command == 'kinzie':
            bot_response = chatgpt_response(prompt=own_message)
            await message.channel.typing()
            await asyncio.sleep(1)
            await message.channel.send(f"{bot_response}")
        
        if message.content.startswith('$meme'):
            meme_url = get_memes()
            await message.channel.send(meme_url)


    
    


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)


        

