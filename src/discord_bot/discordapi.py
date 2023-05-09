from dotenv import load_dotenv
import discord
import os
import asyncio
import random
import emoji
import json
import requests
import pytz
import datetime
from src.chatgpt_bot.openai import turbo_response
from src.chatgpt_bot.openai import chat_response
from src.giphy_bot.giphy import gif_response
from src.giphy_bot.giphy import sticker_response


load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')
discord_user_id = os.getenv('USER_ID')
url_token = os.getenv('GIPHY_API_URL')
emoji_arr = []
all_emoji = [emoji.emojize(x) for x in emoji.EMOJI_DATA]
giphy_attachments = ['mov','gif']


class MyClient(discord.Client):
    async def on_ready(self):
        print("login successful, you are: ", self.user)

        await self.change_presence(activity=discord.Game(name="Saints Row: The Third"), status=discord.Status.online)

        # start the background task to check the time
        client.loop.create_task(self.check_time())

    async def check_time(self):

        # set the timezone to US Eastern Time
        est_tz = pytz.timezone('US/Eastern')

        # set target time to 9 AM 
        target_time = datetime.time(hour=9)

        while True:
            target_date = datetime.datetime.now(tz=est_tz).replace(hour=target_time.hour,
                                                                   minute=target_time.minute,
                                                                   second=target_time.second,
                                                                   microsecond=0)

            # If target time has already passed for today, set target date to tomorrow's date with target time
            if datetime.datetime.now(tz=est_tz) >= target_date:
                target_date += datetime.timedelta(days=1)

            # Wait until target date and time
            await asyncio.sleep((target_date - datetime.datetime.now(tz=est_tz)).total_seconds())
            
            # trigger the action  
            # get the user and create a DM to user
            user = await client.fetch_user(discord_user_id)
            channel = await user.create_dm()
            text_response = chat_response(prompt="Kinzie good morning!")
            await channel.send(f"{text_response}")
    
    async def on_message(self, message):
        print(message.content)
        if message.author == self.user:
            return
        command, own_message=None, None

        for text in ['kinzie', 'bot']:
            if message.content.startswith(text):
                command=message.content.split(' ')[0]
                own_message=message.content.replace(text, '')
                print(command, own_message)

        if command == 'kinzie' or command == 'bot':
            bot_response = turbo_response(prompt=own_message)
            await message.channel.typing()
            await asyncio.sleep(1)
            await message.channel.send(f"{bot_response}")

        for txt in ['Kinzie', 'chat']:
            if message.content.startswith(txt):
                command=message.content.split(' ')[0]
                own_message=message.content.replace(txt, '')
                print(command, own_message)

        if command == 'Kinzie' or command == 'chat':
            text_response = chat_response(prompt=own_message)
            await message.channel.typing()
            await asyncio.sleep(1)
            await message.channel.send(f"{text_response}")

        
        if "Giphy " in message.content:
            await message.channel.send(gif_response(message.content.replace("Giphy ", "")))
        elif "sticker " in message.content:
            await message.channel.send(sticker_response(message.content.replace("sticker ", "")))
        elif any(x in message.content for x in all_emoji):
            range_indexes = range(5)
            for i in range_indexes:
                emoji_arr.append(random.choice(list(emoji.EMOJI_DATA)))
                result = ''.join(emoji_arr)
                result = result[-5:]
            await message.channel.send(result)
        # get if attachment is a .mov file or .gif file
        if message.attachments:
            if any(x in message.attachments[0].filename for x in giphy_attachments):
                meme_url = url_token
                response = requests.get(meme_url)
                response = json.loads(response.text)["data"]["url"]
                await message.channel.send(response)
            else:
                print("There is no attachment")
        
        if message.content.startswith("Search"):
            query = message.content[7:]
            query_string = 'https://duckduckgo.com/?q=' + '+'.join(query.split())
            await message.channel.send(query_string)






    
    


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)


        

