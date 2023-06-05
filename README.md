# Kinzie Discord bot 
In order to use this application you must have python3 and pip3 installed. change into the parent directory and install the requirements.txt file with ```pip3 install -r requirements.txt```

Run the application with ```python3 start.py``` Join your bot to the discord server Copy the bot's token from the discord developer page into the .env file  ```DISCORD_TOKEN``` and ```CHATGPT_API_KEY``` Enjoy your personalized GPT open-source chatbot!

# Instructions for py-kaomoji

make sure pyyaml is installed then

in load_kaomojis.py, add SafeLoader to yaml.load() like so:
```return yaml.load(_f, Loader=yaml.SafeLoader)```



