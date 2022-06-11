import datetime, discord
from discord.ext import commands
from pussybot import cnx, mycursor

'''The setup command'''


class Setup(commands.Cog):
    def __init__(self, bot): self.bot = bot
    
    @commands.command(name="setup", brief="Setup the bot")
    @commands.has_permissions(administrator=True)
    async def _setup(self, ctx, args: discord.TextChannel = None):
        clean = self.bot.get_channel(int(args.id)).name
        """Setup the bot"""
        cnx.reconnect(attempts=3)
        if clean is None:
            embed = discord.Embed(title=f"Setup pussybot", description=f"pussybot could not setup properly. Please check your arguments and try again", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.add_field(name="Usage", value=f"-setup [logging channel]", inline=True)
            embed.set_footer(text=f"Requested by: {ctx.author} | [required] (optional)", icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=embed)
            return    
            
        for channel in ctx.guild.channels:
            if channel.name == clean:
                channel2 = discord.utils.get(ctx.guild.channels, name=clean)
                if type(channel2) != discord.channel.TextChannel:
                    embed = discord.Embed(title=f"Setup pussybot", description=f"pussybot could not setup properly. Please check your arguments and try again", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
                    embed.add_field(name="Error", value=f"AUDIO_CHANNEL_SPECIFIED", inline=True)  
                    embed.set_footer(text=f"Requested by: {ctx.author} | [required] (optional)", icon_url=f"{ctx.author.avatar}")
                    await ctx.reply(embed=embed)
                    return        
                
                global logging
                
                try:
                    try:
                        mycursor.execute(f"DELETE FROM WCTable WHERE ServerID=\"{ctx.guild.id}\";")
                    except: 
                        pass
                    sql = "INSERT INTO WCTable (ServerID, LoggingChannelID) VALUES (%s, %s)"
                    val = (ctx.guild.id, channel2.id)
                    mycursor.execute(sql, val)

                    cnx.commit()
                    if cnx.is_connected(): pass
                    else: cnx.reconnect(attempts=3)

                except:
                    sql = "UPDATE WCTable SET LoggingChannelID = %s WHERE ServerID = %s"
                    val = (channel2.id, ctx.guild.id)
                    mycursor.execute(sql, val)

                    cnx.commit()
                    if cnx.is_connected(): pass
                    else: cnx.reconnect(attempts=3)

                
                embed = discord.Embed(title=f"Setup pussybot", description=f"Channel found, I have sent a message to the provided channel", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
                embed.add_field(name="Channel", value=f"<#{channel2.id}>", inline=True)
                embed.set_footer(text=f"Setup complete", icon_url=f"{ctx.author.avatar}")
                await ctx.reply(embed=embed)
                
                embed2 = discord.Embed(title=f"Setup pussybot", description=f"This is the channel specified", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
                embed2.add_field(name="Set as logging channel", value="Yes", inline=True)
                embed2.set_footer(text=f"Setup complete", icon_url=f"{ctx.author.avatar}")
                try:
                    await channel.send(embed=embed2)
                except discord.errors.Forbidden as e:
                    embed = discord.Embed(title=f"Setup pussybot", description=f"pussybot could not setup properly. Please check your arguments and try again", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
                    embed.add_field(name="Error", value=e, inline=True)
                    embed.set_footer(text=f"Requested by: {ctx.author} | [required] (optional)", icon_url=f"{ctx.author.avatar}")
                    await ctx.reply(embed=embed)
                return 
            
        embed = discord.Embed(title=f"Setup pussybot", description=f"pussybot could not setup properly. Please check your arguments and try again", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
        embed.add_field(name="Error", value=f"INVALID_CHANNEL", inline=True)
        embed.set_footer(text=f"Requested by: {ctx.author} | [required] (optional)", icon_url=f"{ctx.author.avatar}")
        await ctx.reply(embed=embed)
        return         
        
def setup(bot): bot.add_cog(Setup(bot))
print("Setup cog loaded")