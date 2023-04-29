from dotenv import load_dotenv
import discord
import os
import requests
import json

load_dotenv()

giphy_token = os.getenv('GIPHY_URL')

def get_memes():
    url = giphy_token
    giphy_response = requests.get(url)
    return json.loads(giphy_response.text)['data']['url']