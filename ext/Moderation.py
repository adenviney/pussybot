import datetime, discord, lib.database as db
from discord.ext import commands

cum, cursor = db.db.connect("db1")
cbx, csr = db.db.connect("db4")

class Moderation(commands.Cog):
    def __init__(self, bot): self.bot = bot

    #Warn system
    @commands.command(name="warn", brief="Warn a user")
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, user: discord.Member, *, reason: str = "No reason given"):
        if cum.is_connected(): pass
        else: cum.reconnect(attempts=3)
        if user is None:
            await ctx.send(discord.Embed(title=f"You need to specify a user", color=discord.Color.red()))
            return
        embed = discord.Embed(title="Warned", description=f"You have been warned in {ctx.guild.name} for {reason}", color=discord.Color.red())
        await user.send(embed=embed)
        try:
            cursor.execute("SELECT Warns FROM `" + str(ctx.guild.id) + "` WHERE ClientID = " + str(user.id) + ";")
            warns = cursor.fetchone()[0]
            warns += 1
            cursor.execute("UPDATE `" + str(ctx.guild.id) + "` SET Warns = " + str(warns) + " WHERE ClientID = " + str(user.id) + ";")
            cum.commit()
            await ctx.send(embed=discord.Embed(title=f"Warned {user.name}#{user.discriminator}", description=f"Successfully warned {user.name}#{user.discriminator} for {reason}", color=discord.Color.green()))
            if warns == 3:
                try:
                    await ctx.send(embed=discord.Embed(title=f"Kicked {user.name}#{user.discriminator}", description=f"Successfully kicked {user.name}#{user.discriminator} for reaching 3 warns", color=discord.Color.green()))
                    await user.send(embed=discord.Embed(title=f"Kicked", description=f"You have been kicked from {ctx.guild.name} for reaching 3 warns", color=discord.Color.red()))
                    await user.kick(reason=reason)
                except:
                    await ctx.send(embed=discord.Embed(title=f"Failed to kick {user.name}#{user.discriminator}", description=f"Failed to kick {user.name}#{user.discriminator} for reaching 3 warns", color=discord.Color.red()))
            elif warns == 5:
                try:
                    await ctx.send(embed=discord.Embed(title=f"Banned {user.name}#{user.discriminator}", description=f"Successfully banned {user.name}#{user.discriminator} for reaching 5 warns", color=discord.Color.green()))
                    await user.send(embed=discord.Embed(title=f"Banned", description=f"You have been banned from {ctx.guild.name} for reaching 5 warns", color=discord.Color.red()))
                    await user.ban(reason=reason)
                except:
                    await ctx.send(discord.Embed(title=f"Failed to ban {user.name}#{user.discriminator}", description=f"Failed to ban {user.name}#{user.discriminator} for reaching 5 warns", color=discord.Color.red()))
        except:
            #Add user to database
            cursor.execute("INSERT INTO `" + str(ctx.guild.id) + "` (ClientID, Warns) VALUES (" + str(user.id) + ", 1);")
            cum.commit()
            await ctx.send(embed=discord.Embed(title=f"Warned {user.name}#{user.discriminator}", description=f"Successfully warned {user.name}#{user.discriminator} for {reason}", color=discord.Color.green()))
            
    @commands.command(name="warns", brief="Get the number of warns a user has")
    @commands.has_permissions(administrator=True)
    async def warns(self, ctx, user: discord.Member):
        if cum.is_connected(): pass
        else: cum.reconnect(attempts=3)
        if user is None: 
            await ctx.send(discord.Embed(title=f"You need to specify a user", color=discord.Color.red()))
            return
        cursor.execute("SELECT Warns FROM `" + str(ctx.guild.id) + "` WHERE ClientID = " + str(user.id) + ";")
        warns = cursor.fetchone()[0]
        if warns == 0: await ctx.send(embed=discord.Embed(title=f"{user.name}#{user.discriminator} has no warns", color=discord.Color.green()))
        if warns == 1: await ctx.send(embed=discord.Embed(title=f"{user.name}#{user.discriminator} has 1 warn", color=discord.Color.green()))
        else: await ctx.send(embed=discord.Embed(title=f"{user.name}#{user.discriminator} has {warns} warns", color=discord.Color.green()))
        
    @commands.command(name="clearwarns", brief="Clear the warns of a user", aliases=["cwarns", "cw"])
    @commands.has_permissions(administrator=True)
    async def clearwarns(self, ctx, user: discord.Member):
        if cum.is_connected(): pass
        else: cum.reconnect(attempts=3)
        if user is None: 
            await ctx.send(discord.Embed(title=f"You need to specify a user", color=discord.Color.red()))
            return
        cursor.execute("UPDATE `" + str(ctx.guild.id) + "` SET Warns = 0 WHERE ClientID = " + str(user.id) + ";")
        cum.commit()
        await ctx.send(embed=discord.Embed(title=f"Cleared {user.name}#{user.discriminator}'s warns", color=discord.Color.green()))
        
    @commands.command(name="removewarn", brief="Remove a warn from a user", aliases=["rwarn", "rw"])
    @commands.has_permissions(administrator=True)
    async def removewarn(self, ctx, user: discord.Member, amt: int):
        if cum.is_connected(): pass
        else: cum.reconnect(attempts=3)
        if user is None:
            await ctx.send(discord.Embed(title=f"You need to specify a user", color=discord.Color.red()))
            return
        if amt is None:
            await ctx.send(discord.Embed(title=f"You need to specify an amount", color=discord.Color.red()))
            return
        cursor.execute("SELECT Warns FROM `" + str(ctx.guild.id) + "` WHERE ClientID = " + str(user.id) + ";")
        warns = cursor.fetchone()[0]
        if warns == 0:
            await ctx.send(discord.Embed(title=f"{user.name}#{user.discriminator} has no warns", color=discord.Color.green()))
            return
        if amt > warns:
            await ctx.send(discord.Embed(title=f"{user.name}#{user.discriminator} has only {warns} warns", color=discord.Color.green()))
            return
        cursor.execute("UPDATE `" + str(ctx.guild.id) + "` SET Warns = Warns - " + str(amt) + " WHERE ClientID = " + str(user.id) + ";")
        cum.commit()
        await ctx.send(embed=discord.Embed(title=f"Removed {amt} warns from {user.name}#{user.discriminator}", color=discord.Color.green()))
            
        
    @commands.command(name="addrestrictedword", brief="Add a restricted word", aliases=["arw", "arword"])
    @commands.has_permissions(administrator=True)
    async def addrestrictedword(self, ctx, word: str):
        if cbx.is_connected(): pass
        else: cbx.reconnect(attempts=3)
        if word is None:
            await ctx.send(discord.Embed(title=f"You need to specify a word", color=discord.Color.red()))
            return
        csr.execute("SELECT * FROM `RestrictedWords` WHERE Word = '" + word + "';")
        if csr.fetchone() is not None:
            await ctx.send(discord.Embed(title=f"{word} is already a restricted word", color=discord.Color.red()))
            return
        csr.execute("INSERT INTO `RestrictedWords` (Word) VALUES ('" + word + "');")
        cbx.commit()
        await ctx.send(embed=discord.Embed(title=f"Added {word} to the restricted words", color=discord.Color.green()))
        
        
    @commands.command(name="removerestrictedword", brief="Remove a restricted word", aliases=["rrw", "rrword"])
    @commands.has_permissions(administrator=True)
    async def removerestrictedword(self, ctx, word: str):
        if cbx.is_connected(): pass
        else: cbx.reconnect(attempts=3)
        if word is None:
            await ctx.send(discord.Embed(title=f"You need to specify a word", color=discord.Color.red()))
            return
        csr.execute("SELECT * FROM `RestrictedWords` WHERE Word = '" + word + "';")
        if csr.fetchone() is None:
            await ctx.send(discord.Embed(title=f"{word} is not a restricted word", color=discord.Color.red()))
            return
        csr.execute("DELETE FROM `RestrictedWords` WHERE Word = '" + word + "';")
        cbx.commit()
        await ctx.send(embed=discord.Embed(title=f"Removed {word} from the restricted words", color=discord.Color.green()))
        
    @commands.command(name="listrestrictedwords", brief="List the restricted words", aliases=["lrw", "lrwords"])
    @commands.has_permissions(administrator=True)
    async def listrestrictedwords(self, ctx):
        if cbx.is_connected(): pass
        else: cbx.reconnect(attempts=3)
        csr.execute("SELECT * FROM `RestrictedWords`;")
        words = csr.fetchall()
        if len(words) == 0:
            await ctx.send(discord.Embed(title=f"There are no restricted words", color=discord.Color.green()))
            return
        msg = ""
        for word in words:
            msg += word[0] + "\n"
        await ctx.send(embed=discord.Embed(title=f"Restricted words", description=msg, color=discord.Color.green()))
        
        
        
        
    
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
            if e == "400 Bad Request (error code: 50007): Cannot send messages to this user": 
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