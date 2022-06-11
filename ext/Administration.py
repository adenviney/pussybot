import datetime
import discord
import os
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
                if channel.name == "-̗̀➛announcements": pass
                if channel.name == "・rules࿐": pass
                if channel.name == "・roles࿐": pass
                if channel.name == "・color-roles࿐": pass
                if channel.name == "・verify࿐": pass
                if channel.name == "・new-users࿐": pass
                if channel.name == "-̗̀➛giveaways": pass
                
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
            try:
                #if channel is named announcements, skip it
                if channel.name == "-̗̀➛announcements": pass
                if channel.name == "・rules࿐": pass
                if channel.name == "・roles࿐": pass
                if channel.name == "・color-roles࿐": pass
                if channel.name == "・verify࿐": pass
                if channel.name == "・new-users࿐": pass
                if channel.name == "-̗̀➛giveaways": pass
                
                else: await channel.set_permissions(discord.utils.get(ctx.guild.roles, name="Verified"), send_messages=True)
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
        
    # @commands.command(name="rolereact", brief="Send an embed which will allow a user to gain a role off of reacting")
    # @commands.has_permissions(administrator=True)
    # #$rr <message> role|emoji role|emoji role|emoji
    # async def rolereact(self, ctx, *, args):
    #     #args will look like "React to gain role^348324830928|:fish: 32784023947032974|:fish:"
    #     if ctx.message.author.guild_permissions.administrator == False:
    #         embed = discord.Embed(title=f"❌ Could not send role react", description=f"Failed to execute", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
    #         embed.add_field(name="Error", value="You do not have the permission to manage channels", inline=True)
    #         embed.set_footer(text=f"Attempted by {ctx.author}")
    #         await ctx.reply(embed=embed)
    #         return
    #     #Split the args into a list
    #     message = args.split("^")
    #     spaces = message[1].split(" ")
        
    #     #Create the embed
    #     embed = discord.Embed(title=message[0], color=0x2F3136)
    #     #Send the embed
    #     msg = await ctx.reply(embed=embed)
        
    #     #loop through all indexes in list and strip them of whitespace
    #     for i in range(len(spaces)):
    #         spaces[i] = spaces[i].strip()
    #         fin = spaces[i].split("|")
    #         await msg.add_reactions(fin[1])
        
        
        
        # print(spaces)

def setup(bot): bot.add_cog(Administration(bot))
print("Administration cog loaded")