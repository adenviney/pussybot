import datetime, discord, os, lib.color as c
from pussybot import bot
from discord.ext import commands

class Administration(commands.Cog):

    def __init__(self, bot): self.bot = bot
    
    @commands.command(name="emergency", brief="Developer command. Restricts bot to only basic commands")
    @commands.has_permissions(administrator=True)
    async def emergency(self, ctx):
        await ctx.send(embed=discord.Embed(title=f"Emergency mode enabled", description="$restore to unlock commands again", timestamp=datetime.datetime.utcnow(), color=discord.Color.green()))
        os.system("python ./lib/emergency.py")
    
    @commands.command(name="lockdown", brief="Lockdown the server")
    #@commands.has_permissions(manage_guild=True)
    async def lockdown(self, ctx, *, reason="No reason provided"):
        if ctx.message.author.guild_permissions.manage_guild == False:
            embed = discord.Embed(title=f"❌ Could not lockdown server", description=f"Failed to execute", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.add_field(name="Error", value="You do not have the permission to manage channels", inline=True)
            embed.set_footer(text=f"Attempted by {ctx.author}")
            await ctx.reply(embed=embed)
            return
        for channel in ctx.guild.channels:
            try:
                await channel.set_permissions(discord.utils.get(ctx.guild.roles, name="Verified"), send_messages=False)
            except Exception as e:
                if e == "403 Forbidden (error code: 50013): Cannot modify send_messages": 
                    continue
                embed = discord.Embed(title=f"❌ Could not lockdown {channel}", description=f"Failed to execute", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
                embed.add_field(name="Error", value=e, inline=True)
                embed.set_footer(text=f"Attempted by {ctx.author}")
                await ctx.reply(embed=embed)
        
        #Send the lockdown embed
        embed = discord.Embed(title=f"🔒 Server locked down", description=f"Executed successfully", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
        embed.add_field(name="Reason", value=reason, inline=True)
        embed.set_footer(text=f"Locked down by {ctx.author}")
        await ctx.reply(embed=embed)
        
    @commands.command(name="unlock", brief="Unlock the server")
    @commands.has_permissions(manage_guild=True)
    async def unlock(self, ctx, *, reason="No reason provided"):
        if ctx.message.author.guild_permissions.manage_guild == False:
            embed = discord.Embed(title=f"❌ Could not unlock server", description=f"Failed to execute", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.add_field(name="Error", value="You do not have the permission to manage channels", inline=True)
            embed.set_footer(text=f"Attempted by {ctx.author}")
            await ctx.reply(embed=embed)
            return
        for channel in ctx.guild.channels:
            restricted_channels = [939011378956603452, 938973141919752202, 939000498084782150, 939613231574573167, 983381315804069989, 983392113746141204, 982828063379325008]
            try:
                if channel.id in restricted_channels: await channel.set_permissions(discord.utils.get(ctx.guild.roles, name="Verified"), send_messages=False)
                else:  await channel.set_permissions(discord.utils.get(ctx.guild.roles, name="Verified"), send_messages=True)
            except Exception as e:
                embed = discord.Embed(title=f"❌ Could not unlock {channel}", description=f"Failed to execute", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
                embed.add_field(name="Error", value=e, inline=True)
                embed.set_footer(text=f"Attempted by {ctx.author}")
                await ctx.reply(embed=embed)
        
        #Send the unlock embed
        embed = discord.Embed(title=f"🔓 Server unlocked", description=f"Executed successfully", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
        embed.add_field(name="Reason", value=reason, inline=True)
        embed.set_footer(text=f"Unlocked by {ctx.author}")
        await ctx.reply(embed=embed)

def setup(bot): bot.add_cog(Administration(bot))
print(c.color.GREEN + "Administration cog loaded" + c.color.END)