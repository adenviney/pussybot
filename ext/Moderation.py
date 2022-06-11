import datetime, discord, mysql.connector, json
from discord.ext import commands
from discord.ext import tasks


with open('database-conf.json') as f:
    config = json.load(f)

try: #Everything
    cum = mysql.connector.connect(**config)
    cursor = cum.cursor()
    print(f"Connected to {config['user']}")
except mysql.connector.Error as err: print("You fucked up lmao" + str(err))

class Moderation(commands.Cog):
    def __init__(self, bot): self.bot = bot
        
    #TODO: Add mute/unmute, purge, auto moderation and custom filtered words

    #Warn system
    # @commands.command(name="warn", brief="Warn a user")
    # @commands.has_permissions(administrator=True)
    # async def warn(self, ctx, user: discord.Member, *, reason: str):
    #     if cum.is_connected(): pass
    #     else: cum.reconnect(attempts=3)
    #     cursor.execute("SELECT Warns FROM `" + str(ctx.guild.id) + "` WHERE ClientID = " + str(user.id) + ";")
    #     warns = cursor.fetchone()
    #     if warns[0] is None: warns = 0
    #     else: warns = warns[0]
    #     warns = warns + 1
    #     cursor.execute("UPDATE `" + str(ctx.guild.id) + "` SET Warns = " + str(warns) + " WHERE ClientID = " + str(user.id) + ";")
    #     cum.commit()
    #     embed = discord.Embed(title="Warned", description=f"You have been warned in {ctx.guild.name} for {reason}", color=0x8E72BE)
    #     await user.send(embed=embed)
    #     await ctx.send(f"{user.mention} has been warned for {reason}")      
    
    @commands.command(name="mute", brief="Mute a user")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason: str = "No reason given"):
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            await member.add_roles(role) 
            embed = discord.Embed(description= f"✅ **{member.name}#{member.discriminator} muted successfully**", color=discord.Color.green())
            await ctx.send(embed=embed)
            
    @commands.command(name="unmute", brief="Unmute a user")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason: str = "No reason given"):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(role)
        embed = discord.Embed(description= f"✅ **{member.name}#{member.discriminator} unmuted successfully**", color=discord.Color.green())
        await ctx.send(embed=embed)
            

    @commands.command(name="purge", brief="Purge a number of messages")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amt: int):
        if amt > 100:
            await ctx.send("You can't delete more than 100 messages at once")
            return
        await ctx.channel.purge(limit=amt)
        await ctx.send(embed=discord.Embed(title=f"Deleted {amt} messages", color=discord.Color.green()))
            
    @commands.command(name="kick", brief="Kick a user from the server")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        try:
            await member.kick(reason=reason)
            memberE = discord.Embed(title=f"You have been kicked from {ctx.guild.name} | {reason}", color=discord.Color.red())
            await member.send(embed=memberE)
            embed = discord.Embed(title=f"✅ Kicked {member} ({member.id})", description=f"Executed successfully", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
            embed.add_field(name="Reason", value=reason, inline=True)
            embed.set_footer(text=f"Kicked by {ctx.author}", icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=embed)
        except Exception as e:
            if e == "403 Forbidden (error code: 50007): Cannot send messages to this user": 
                await member.kick(reason=reason)
                embed = discord.Embed(title=f"✅ Kicked {member} ({member.id})", description=f"Executed successfully", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
                embed.add_field(name="Reason", value=reason, inline=True)
                embed.set_footer(text=f"Kicked by {ctx.author}", icon_url=f"{ctx.author.avatar}")
                await ctx.reply(embed=embed)
                return
            embed = discord.Embed(title=f"❌ Could not kick {member} ({member.id})", description=f"Failed to execute", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.add_field(name="Error", value=e, inline=True)
            embed.set_footer(text=f"Attempted by {ctx.author}", icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=embed)

    @commands.command(name="ban", brief="Ban a user from the server")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        try:
            await member.ban(reason=reason)
            memberE = discord.Embed(title=f"You have been banned from {ctx.guild.name} | {reason}", color=discord.Color.red())
            await member.send(embed=memberE)
            embed = discord.Embed(title=f"✅ Banned {member} ({member.id})", description=f"Executed successfully", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
            embed.add_field(name="Reason", value=reason, inline=True)
            embed.set_footer(text=f"Banned by {ctx.author}", icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=embed)
        except Exception as e:
            if e == "403 Forbidden (error code: 50007): Cannot send messages to this user": 
                await member.ban(reason=reason)
                embed = discord.Embed(title=f"✅ Banned {member} ({member.id})", description=f"Executed successfully", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
                embed.add_field(name="Reason", value=reason, inline=True)
                embed.set_footer(text=f"Banned by {ctx.author}", icon_url=f"{ctx.author.avatar}")
                await ctx.reply(embed=embed)
                return
            embed = discord.Embed(title=f"❌ Could not ban {member} ({member.id})", description=f"Failed to execute", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.add_field(name="Error", value=e, inline=True)
            embed.set_footer(text=f"Attempted by {ctx.author}", icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=embed)

    @commands.command(name="unban", brief="Unban a user from the server")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        bannedUsers = await ctx.guild.bans()
        memberName, memberDiscriminator = member.split('#')
        
        try:
            for banEntry in bannedUsers:
                user = banEntry.user
                
                if (user.name, user.discriminator) == (memberName, memberDiscriminator):
                    await ctx.guild.unban(user)
                    embed = discord.Embed(title=f"✅ Unbanned {member}", description=f"Executed successfully", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
                    embed.set_footer(text=f"Unbanned by {ctx.author}", icon_url=f"{ctx.author.avatar}")
                    await ctx.reply(embed=embed)
                    return
                
        except Exception as e:     
            embed = discord.Embed(title=f"❌ Could not unban {member}", description=f"Failed to execute", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.add_field(name="Error", value=e, inline=True)
            embed.set_footer(text=f"Unban attempted by {ctx.author}", icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=embed)
            return

    @ban.error
    async def ban_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title=f"❌ Could not ban that user", description=f"Failed to execute", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.add_field(name="Error", value="You do not have permission to ban members", inline=True)
            embed.set_footer(text=f"Attempted by {ctx.author}", icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=embed)

    @kick.error
    async def kick_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title=f"❌ Could not kick that user", description=f"Failed to execute", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.add_field(name="Error", value="You do not have permission to kick members", inline=True)
            embed.set_footer(text=f"Attempted by {ctx.author}", icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=embed)
            
    @unban.error
    async def unban_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title=f"❌ Could not unban that user", description=f"Failed to execute", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.add_field(name="Error", value="You do not have permission to unban members", inline=True)
            embed.set_footer(text=f"Attempted by {ctx.author}", icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=embed)
        
def setup(bot): bot.add_cog(Moderation(bot))
print("Moderation cog loaded")