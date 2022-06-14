import os, discord, json
from discord.ext import commands

VERSION = "0.8.7"
PATCHNOTES = f"""Pussybot v{VERSION} patchnotes
[!] Open source code is available on GitHub: https://github.com/adenviney/pussybot

[+] Stocks update, $stocks, $invest!
"""

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', description="coolowo", intents=intents, help_command=None)

for extension in os.listdir("./ext"):
    if extension.endswith('.py'):
        try:
            bot.load_extension(f'ext.{extension[:-3]}')
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

print('Initialized')
with open("./json/tkn.json") as f: 
    token = json.load(f)["token"]
    
bot.run(f"{token}")