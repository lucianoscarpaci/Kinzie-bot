# import the discord client and api token from discord api
from src.discord_bot.discordapi import client, discord_token

if __name__ == '__main__':
    client.run(discord_token)