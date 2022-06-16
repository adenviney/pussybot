import os, discord, json, lib.color as c
from discord.ext import commands

VERSION = "0.8.7"
PATCHNOTES = f"""Pussybot v{VERSION} patchnotes
[!] Open source code is available on GitHub: https://github.com/adenviney/pussybot

[*] Fixed more bugs, blackjack update! $blackajck, bj <bet>
"""

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', description="coolowo", intents=intents, help_command=None)

for extension in os.listdir("./ext"):
    if extension.endswith('.py'):
        try:
            bot.load_extension(f'ext.{extension[:-3]}')
            print(c.color.GREEN + f"ext.{extension[:-3]} loaded" + c.color.END)
        except Exception as e:
            print(c.color.FAIL + f'Failed to load extension {extension}\n{type(e).__name__}: {e}' + c.color.END)

print('Initialized')
with open("./json/tkn.json") as f: 
    token = json.load(f)["token"]
    

bot.run(f"{token}")