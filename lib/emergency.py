import os, discord, datetime, json
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', description="coolowo", intents=intents, help_command=None)

@bot.command()
@commands.has_permissions(administrator=True)
async def restore(ctx):
    await ctx.send(embed=discord.Embed(title=f"Emergency mode disabled", description="$emergency to restrict commands again", timestamp=datetime.datetime.utcnow(), color=discord.Color.green()))
    os.system("python pussybot.py")

print('BOT RESTARTED IN EMERGENCY MODE, RUN COMMAND $RESTORE TO RESTORE BACK')            
with open("../tkn.json") as f: token = json.load(f)["token"]
bot.run(token)