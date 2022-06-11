import contextlib, datetime, io, textwrap, discord
from traceback import format_exception
from pussybot import bot
from discord.ext import commands
from lib.evalcc import *

class Owner(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot
        self.developers = {
            751255963805155438,
            955629544650465340
        }
        
    @commands.command(name="eval", aliases=["exec", "evaluate"], brief="Evaluate code")
    @commands.is_owner() #Change this and you're fucked
    async def _eval(self, ctx, *, code):
        """Evaluate commands."""
        code = cleancode(code)

        local_variables = {
            "discord": discord,
            "commands": commands,
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message
        }

        stdout = io.StringIO()
        
        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
                )

                obj = await local_variables["func"]()
                result = f"{stdout.getvalue()}\n-- {obj}\n"
        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))

        pager = Pag(
            timeout=100,
            entries=[result[i: i + 2000] for i in range(0, len(result), 2000)],
            length=1,
            prefix="```python\n",
            suffix="```"
        )

        await ctx.message.add_reaction('✅')
        await pager.start(ctx)

    @commands.command(name="shutdown", brief="Shutdown the bot", aliases=["shtdwn"])
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shutdown the bot."""
        await ctx.send("Developer shutdown: Initiating.")
        exit()
        
    @commands.command(name="toggle", brief="Enable/Disable a command")
    @commands.is_owner()
    async def toggle(self, ctx, *, command):
        """Toggle a command."""
        command = bot.get_command(command)
        
        if command is None: await ctx.send(discord.Embed(title=f"That command doesn't exist", timestamp=datetime.datetime.utcnow(), color=discord.Color.red()))
        elif ctx.command == command: await ctx.send(discord.Embed(title=f"You cannot disable the toggle command", timestamp=datetime.datetime.utcnow(), color=discord.Color.red()))
        else:
            command.enabled = not command.enabled
            ternary = 'Enabled' if command.enabled else 'Disabled'
            color = discord.Color.green() if command.enabled else discord.Color.red()
            await ctx.send(embed=discord.Embed(title=f"{ternary} {command.qualified_name}", timestamp=datetime.datetime.utcnow(), color=color))
            
    @commands.command(name="reload", brief="Reload a cog")
    @commands.is_owner()
    async def reload(self, ctx, *, cog):
        cog = cog.lower()
        if cog in self.bot.cogs:
            self.bot.reload_extension(cog)
            await ctx.send(discord.Embed(title=f"Reloaded {cog}", timestamp=datetime.datetime.utcnow(), color=discord.Color.green()))
        else: await ctx.send(discord.Embed(title=f"That cog doesn't exist", timestamp=datetime.datetime.utcnow(), color=discord.Color.red()))
        
    @commands.command(name="authorise", brief="Authorise a user to use developer commands")
    @commands.is_owner()
    async def authorise(self, ctx, user: discord.Member):
        if user.id in self.developers:
            self.developers.remove(user.id)
            await ctx.send(embed=discord.Embed(title=f"{user.name} is no longer authorised to use developer commands", timestamp=datetime.datetime.utcnow(), color=discord.Color.red()))
        else:
            self.developers.add(user.id)
            await ctx.send(embed=discord.Embed(title=f"{user.name} is now authorised to use developer commands", timestamp=datetime.datetime.utcnow(), color=discord.Color.green()))
            
    @commands.command(name="fix", brief="Developer command. Gives all users the verified role")
    @commands.is_owner()
    async def fix(self, ctx):
        await ctx.send(embed=discord.Embed(title=f"Fixing... this may take a while", timestamp=datetime.datetime.utcnow(), color=discord.Color.green()))
        for user in ctx.guild.members:
            print(user)
            if user.id == bot.user.id: continue
            if not user.bot: await user.add_roles(discord.utils.get(ctx.guild.roles, name="Verified"))
        await ctx.reply(embed=discord.Embed(title=f"All users in {ctx.guild.name} now have the verified role", timestamp=datetime.datetime.utcnow(), color=discord.Color.green()))

def setup(bot): bot.add_cog(Owner(bot))
print("Owner cog loaded")