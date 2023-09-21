from config import Config
from banner import Banner
from discord.ext import commands
from colorama import Fore, Style, init
import asyncio
import random
import json
import re
import datetime
import os

init()
current_datetime = datetime.datetime.now()
timestamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

def find_word(words, user_input):
    for word in words:
        if len(word) != len(user_input):
            continue
        match = True
        for i in range(len(word)):
            if user_input[i] != '_' and user_input[i] != word[i]:
                match = False
                break
        if match:
            return word   
    return None

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.YELLOW, Banner.get_banner(), Style.RESET_ALL)

def start():
    bot = commands.Bot(command_prefix='!')

    async def send_message(channel_id, message):
        try:
            channel = bot.get_channel(int(channel_id))
            await channel.send(message)
        except Exception as e:
            print(f"{Fore.RED}Error in send_message: {e}{Style.RESET_ALL}")

    @bot.event
    async def on_ready():
        print_banner()
        print(f'[{timestamp}] [INFO] - {Fore.LIGHTGREEN_EX}Logged on as {bot.user}{Style.RESET_ALL}')
        print(f'[{timestamp}] [INFO] - {Fore.LIGHTGREEN_EX}Bot Is Ready...{Style.RESET_ALL}')
        print(f'[{timestamp}] [INFO] - Start Spamming...')
        pause = False
        while True:
            if not pause:
                timer = random.uniform(1.5, 3)
                await send_message(Config.spam_channel, 'Buy Premuim Version Only 10$ <@1118077275330596957>')
                await asyncio.sleep(timer)
            else:
                await asyncio.sleep(5)
                pause = False

    @bot.event
    async def on_message(message):
        try:
            poketwo = 716390085896962058

            if message.channel.id == int(Config.spawn_channel):
                if message.author.id == int(poketwo):
                    if message.embeds:
                        embed_title = message.embeds[0].title
                        if 'wild pokémon has appeared!' in embed_title:
                            timer = random.uniform(1.5, 3)
                            await asyncio.sleep(timer)
                            await message.channel.send('<@716390085896962058> h')
                            pause = True

            if message.author.id == int(poketwo) and message.channel.id == int(Config.spawn_channel):
                if message.content.startswith('The pokémon is '):
                    extracted_word = message.content[len('The pokémon is '):].strip('.').strip().replace('\\', '')
                    print(f'[{timestamp}] [HINT] - {Fore.YELLOW}Pokemon Hint: {Style.RESET_ALL}{extracted_word}')
                    result = find_word(words, extracted_word)
                    if result:
                        await message.channel.send(f'<@716390085896962058> c {result}')
                        print(f"[{timestamp}] [HINT] - {Fore.LIGHTGREEN_EX}Search Result: {Style.RESET_ALL}{result}")
                    else:
                        print(f"[{timestamp}] [ERROR] - {Fore.RED}Pokemon Not Founded In Database{Style.RESET_ALL}")

            if message.author.id == int(poketwo) and message.channel.id == int(Config.spawn_channel):
                if message.content.startswith('Congratulations'):
                    match = re.search(r'Congratulations <@\d+>! (.+)', message.content)
                    if match:
                        extracted_message = match.group(1)
                        print(f'[{timestamp}] [INFO] - {Fore.LIGHTGREEN_EX}{extracted_message}{Style.RESET_ALL}')
                elif message.content.startswith('That is the wrong pokémon!'):
                    print(f'[{timestamp}] [INFO] - {Fore.RED}That is the wrong pokémon!{Style.RESET_ALL}')

        except Exception as e:
            print(f"[{timestamp}] [ERROR] - {Fore.RED}Error in on_message: {Style.RESET_ALL}{e}")


    with open('pokemon.json', 'r', encoding='utf-8') as f:
        words = json.load(f)

    bot.run(Config.token)

start()
