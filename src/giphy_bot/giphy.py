from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

giphy_token = os.getenv('GIPHY_URL')
giphy_token_2 = os.getenv('GIPHY_CATS_URL')
giphy_token_3 = os.getenv('GIPHY_TRIPPY_URL')

def get_memes():
    url = giphy_token
    giphy_response = requests.get(url)
    return json.loads(giphy_response.text)['data']['url']

def get_cat_memes():
    cats_url = giphy_token_2
    giphy_response = requests.get(cats_url)
    return json.loads(giphy_response.text)['data']['url']

def get_trippy_memes():
    trippy_url = giphy_token_3
    giphy_response = requests.get(trippy_url)
    return json.loads(giphy_response.text)['data']['url']