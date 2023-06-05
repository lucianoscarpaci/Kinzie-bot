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
        target_time = datetime.time(hour=9, minute=0, second=0, microsecond=0)



        while True:
            target_date = datetime.datetime.now(tz=est_tz).replace(hour=target_time.hour,
                                                                   minute=target_time.minute,
                                                                   second=target_time.second,
                                                                   microsecond=0)

            # If target time has already passed for today, set target date to tomorrow's date with target time
            if datetime.datetime.now(tz=est_tz) >= target_date:
                target_date += datetime.timedelta(days=1)
                # Update flag to indicate action has been triggered
                print(target_date)

            # Wait until target time is reached
            await asyncio.sleep((target_date - datetime.datetime.now(tz=est_tz)).total_seconds())

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

            # wait for 60 seconds before checking again
            await asyncio.sleep(60)

    async def on_message(self, message):
        
        # if the message is from the bot itself, ignore it
        if message.author == self.user:
            return

        if message.content.startswith("show keys"):
            await message.channel.send("```⁇: Turbo Response\n。: Chat Response\n°: Gif Response\n```")

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
        # emoji section
        all_emoji = [emoji.emojize(x) for x in emoji.EMOJI_DATA]
        if any(x in message.content for x in all_emoji):
            my_message = message.content
            emoji_response = chat_response(prompt=my_message + "In your response include emojis to describe how you feel about me.\n")
            await message.channel.send(f"{emoji_response}")
        # kaomoji section
        kao = kaomoji.Kaomoji()
        all_kaomoji = [x for x in kao.all_kaomoji()]
        if any(x in message.content for x in all_kaomoji):
            kaomoji_message = message.content
            # testing kaomoji response
            kaomoji_response = chat_response(prompt=kaomoji_message + "In your response include one kaomoji to express how you feel about me.\n")
            await message.channel.send(f"{kaomoji_response}")
        # get if attachment is a .mov file or .gif file
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


