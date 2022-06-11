import os, discord, mysql.connector, json
from discord.ext import commands

VERSION = "0.8.2"
PATCHNOTES = f"""Pussybot v{VERSION} patchnotes

[!] Open source code is available on GitHub: https://github.com/adenviney/pussybot

"""

with open('database-conf.json') as f:
    config = json.load(f)

try: #Everything
    cnx = mysql.connector.connect(**config)
    mycursor = cnx.cursor()
    print(f"Connected to {config['user']}")
except mysql.connector.Error as err: #This is fine
    print("You fucked up lmao" + err)
print("Loaded setup database successfully")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', description="coolowo", intents=intents, help_command=None)

for extension in os.listdir("./ext"):
    if extension.endswith('.py'):
        try:
            bot.load_extension(f'ext.{extension[:-3]}')
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

print('Initialized')
with open("tkn.json") as f: 
    token = json.load(f)["token"]
    
bot.run(f"{token}")