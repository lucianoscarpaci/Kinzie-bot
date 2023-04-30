from dotenv import load_dotenv
import os
import random
import giphy_client
from giphy_client.rest import ApiException

load_dotenv()

giphy_token = os.getenv('GIPHY_API_KEY')

api_instance = giphy_client.DefaultApi()

def search_gifs(query):
    try:
        return api_instance.gifs_search_get(giphy_token, query,
                                            limit=5, rating='r',
                                            lang=["en"]
                                               )
    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e
    
def gif_response(emotion):
    try:
        gifs = search_gifs(emotion)
        lst = list(gifs.data)
        gif = random.choices(lst)
        return gif[0].url
    except IndexError:
        return "Cannot find anything similar. Try again!"

def search_stickers(query):
    try:
        return api_instance.stickers_search_get(giphy_token, query,
                                            limit=5, rating='r',
                                            lang=["en"])

    except ApiException as e:
        return "Exception when calling DefaultApi->stickers_search_get: %s\n" % e
    
def sticker_response(emotion):
    try:
        stickers = search_stickers(emotion)
        lst = list(stickers.data)
        sticker = random.choices(lst)

        return sticker[0].url
    except IndexError:
        return "Cannot find anything similar. Try again!"
    