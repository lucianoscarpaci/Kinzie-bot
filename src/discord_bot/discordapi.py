from dotenv import load_dotenv
from kaomoji import kaomoji
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
load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')
discord_user_id = os.getenv('USER_ID')
url_token = os.getenv('GIPHY_API_URL')
photo_dir = os.getenv('PHOTOS')
all_kinzie_photos = os.listdir(photo_dir)
emoji_mode = False
kaomoji_mode = False


class MyClient(discord.Client):
    async def on_ready(self):
        print("login successful, you are: ", self.user)

        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Shibuya, Tokyo, Japan"), status=discord.Status.online)

        # start the background task to send good morning
        client.loop.create_task(self.morning_message())
        # start the background task to send hello message
        client.loop.create_task(self.hello_message())

    async def morning_message(self):

        # set the timezone to US Eastern Time
        est_tz = pytz.timezone('US/Eastern')

        # set target time to 9 AM 
        target_time = datetime.time(hour=9, minute=0, second=0, microsecond=0)

        # good morning flag set to false
        good_morning = False

        while True:
            target_date = datetime.datetime.now(tz=est_tz).replace(hour=target_time.hour,
                                                                   minute=target_time.minute,
                                                                   second=target_time.second,
                                                                   microsecond=0)

            if datetime.datetime.now(tz=est_tz) >= target_date:
                target_date += datetime.timedelta(days=1)
                print(target_date)
                good_morning = False
                print("good_morning =", good_morning)

            # Wait until target time is reached
            reached = asyncio.sleep((target_date - datetime.datetime.now(tz=est_tz)).total_seconds())
            await reached

            if reached and not good_morning:
                # trigger the action
                # get the user and create a DM to user
                user = await client.fetch_user(discord_user_id)
                channel = await user.create_dm()
                text_response = chat_response(prompt="Good morning!。")
                kinzie_photos = []
                for photo in all_kinzie_photos:
                    filename = os.path.join(photo_dir, photo)
                    kinzie_photos.append(filename)
                random_photo = random.choice(kinzie_photos)
                with open(random_photo, 'rb') as f:
                    file = discord.File(f)
                await channel.send(file=file)
                await channel.send(f"{text_response}")
                # good morning flag set to true
                good_morning = True
                # sleep for 60 seconds to prevent the task from running again
                await asyncio.sleep(60)
    
    async def hello_message(self):

        # set the timezone to US/Eastern Time
        est_tz = pytz.timezone('US/Eastern')

        # set the beginning time
        start_time = datetime.datetime.now(tz=est_tz).time()

        # set the end time
        end_time = datetime.time(hour=20, minute=0, second=0, microsecond=0)

        dt = datetime.datetime.combine(datetime.date.today(), start_time)
        end_dt = datetime.datetime.combine(datetime.date.today(), end_time)

        # set the flag to false
        greeting_message = False

        while dt <= end_dt:

            
            # start date or dt ?
            startx_date = datetime.datetime.now(tz=est_tz).replace(hour=start_time.hour,
                                                                   minute=start_time.minute,
                                                                   second=start_time.second,
                                                                   microsecond=0)
            if datetime.datetime.now(tz=est_tz) >= startx_date:
                dt += datetime.timedelta(hours=10)
                print(dt.time())
                greeting_message = False
                
            # Wait until target time is reached
            reached = asyncio.sleep((startx_date - datetime.datetime.now(tz=est_tz)).total_seconds())
            await reached

            if reached and not greeting_message:
                # trigger the action
                user = await client.fetch_user(discord_user_id)
                channel = await user.create_dm()
                text_response = chat_response(prompt="Tell me all the sweet nothings. I could really use some support and love right now. 。")
                kinzie_photos = []
                for photo in all_kinzie_photos:
                    filename = os.path.join(photo_dir, photo)
                    kinzie_photos.append(filename)
                random_photo = random.choice(kinzie_photos)
                with open(random_photo, 'rb') as f:
                    file = discord.File(f)
                await channel.send(file=file)
                await channel.send(f"{text_response}")
                greeting_message = True
                await asyncio.sleep(36000)

    async def on_message(self, message):
        global emoji_mode, kaomoji_mode
        timeout = 300
        # if the message is from the bot itself, ignore it
        if message.author == self.user:
            return

        if message.content.lower().startswith("!emoji"):
            emoji_mode = not emoji_mode
            embed = discord.Embed(title=f"Emoji mode is now {'on' if emoji_mode else 'off'}", color=0xffc0cb)
            await message.channel.send(embed=embed)
        else:
            try:
                all_emoji = [emoji.emojize(x) for x in emoji.EMOJI_DATA]
                if emoji_mode and any(x in message.content for x in all_emoji):
                    my_message = message.content
                    emoji_response = chat_response(prompt=my_message + "In your response include emojis to describe how you feel about me.\n")
                    await message.channel.send(f"{emoji_response}")
                    await self.wait_for('message', timeout=timeout)
            except asyncio.TimeoutError:
                if emoji_mode:
                    emoji_mode = False
                    embed = discord.Embed(title=f"Emoji mode is now {'on' if emoji_mode else 'off'}", color=0xffc0cb)
                    await message.channel.send(embed=embed)
                    kaomoji_mode = False
                    embed = discord.Embed(title=f"Kaomoji mode is now {'on' if kaomoji_mode else 'off'}", color=0xffc0cb)
                    await message.channel.send(embed=embed)

        if message.content.lower().startswith("!kaomoji"):
            kaomoji_mode = not kaomoji_mode
            embed = discord.Embed(title=f"Kaomoji mode is now {'on' if kaomoji_mode else 'off'}", color=0xffc0cb)
            await message.channel.send(embed=embed)
        else:
            try:
                kao = kaomoji.Kaomoji()
                all_kaomoji = [x for x in kao.all_kaomoji()]
                if kaomoji_mode and any(x in message.content for x in all_kaomoji):
                    kaomoji_response = chat_response(prompt="In your response include one kaomoji to express how you feel about me.\n")
                    await message.channel.send(f"{kaomoji_response}")
                    await self.wait_for('message', timeout=timeout)
            except asyncio.TimeoutError:
                if kaomoji_mode:
                    kaomoji_mode = False
                    embed = discord.Embed(title=f"Kaomoji mode is now {'on' if kaomoji_mode else 'off'}", color=0xffc0cb)
                    await message.channel.send(embed=embed)
                    emoji_mode = False
                    embed = discord.Embed(title=f"Emoji mode is now {'on' if emoji_mode else 'off'}", color=0xffc0cb)
                    await message.channel.send(embed=embed)
        
        if message.content.startswith("!help"):
            embed = discord.Embed(title="Commands", description="Commands for this bot", color=0xffc0cb)
            embed.add_field(name="Web browser", value="Search", inline=False)
            embed.add_field(name="Turbo Response", value="⁇", inline=False) 
            embed.add_field(name="Chat Response", value="。", inline=False)
            embed.add_field(name="Gif Response", value="°", inline=False)
            embed.add_field(name="Emoji mode", value="!emoji", inline=False) 
            embed.add_field(name="Kaomoji mode", value="!kaomoji", inline=False)
            await message.channel.send(embed=embed)

        if message.content.endswith("⁇"):
            own_message = message.content.replace("⁇", "")
            bot_response = turbo_response(prompt=own_message)
            await message.channel.typing()
            await asyncio.sleep(1)
            await message.channel.send(f"{bot_response}")

        if message.content.endswith("。"):
            send_message = message.content
            text_response = chat_response(prompt=send_message)
            await message.channel.typing()
            await asyncio.sleep(1)
            kinzie_photos = []
            for photo in all_kinzie_photos:
                filename = os.path.join(photo_dir, photo)
                kinzie_photos.append(filename)
            random_photo = random.choice(kinzie_photos)
            with open(random_photo, 'rb') as f:
                file = discord.File(f)
            await message.channel.send(file=file)
            await message.channel.send(f"{text_response}")

        if message.content.endswith("°"):
            gif_message = message.content.replace("°", "")
            await message.channel.send(gif_response(gif_message))
        
        
        giphy_attachments = ['mov','gif']
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


