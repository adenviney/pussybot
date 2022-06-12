import lib.color as c
from discord.ext import commands
from pussybot import bot, PATCHNOTES
from lib.evalcc import *

class General(commands.Cog):
    def __init__(self, bot): self.bot = bot
        
    @commands.command(name="ping", brief="Ping the bot and get the latency")
    async def ping(self, ctx): await ctx.send(f"Pong! `{round(bot.latency * 1000)}ms`")
    
    @commands.command(name="patchnotes", brief="Get the latest patchnotes")
    async def patchnotes(self, ctx): 
        embed = discord.Embed(title="Patch notes", description=f"```ini\n{PATCHNOTES}```", color=0x8E72BE)
        await ctx.send(embed=embed)
    
def setup(bot): bot.add_cog(General(bot))
print(c.color.GREEN + "General cog loaded" + c.color.END)