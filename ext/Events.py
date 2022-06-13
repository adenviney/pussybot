import datetime, discord, requests, re, random,  mysql.connector, json, os, lib.color as c
from discord.ext import commands
from pussybot import bot, VERSION


#Database checks whether the user code is their code.
with open('./json/database-conf3.json') as f:
    config = json.load(f)

try: #Everything
    xd = mysql.connector.connect(**config)
    roux = xd.cursor()
except mysql.connector.Error as err: print(c.color.FAIL + "[ERROR] " + c.color.END + str(err))

with open('./json/database-conf4.json') as f:
    config2 = json.load(f)
    
try: #Everything
    cbx = mysql.connector.connect(**config2)
    csr = cbx.cursor()
except mysql.connector.Error as err: print(c.color.FAIL + "[ERROR] " + c.color.END + str(err))

class Events(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot
        self.version = VERSION
        self.max_window = 5
        self.window_time_ms = 5000
    
    @commands.Cog.listener()
    async def on_ready(self):
        await bot.change_presence(activity=discord.Game(name="$help"))
        print("Logged in as: " + bot.user.name + "#" + bot.user.discriminator + " (" + str(bot.user.id) + ")")
        print("Version: " + self.version)
        channel = bot.get_channel(938963082573643806)
        
        embed = discord.Embed(title=f"✅ pussybot started successfully | $patchnotes", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
        embed.add_field(name="Console", value=f"```ini\nAll dependencies up-to-date & installed\nConnected to all databases\nAll cogs loaded\nLogged in as: {bot.user.name}#{bot.user.discriminator}\nReady, version {self.version}```", inline=True)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        xd.reconnect(attempts=3)
        random_code = random.randint(100000, 999999)
        channel = bot.get_channel(983381315804069989)
        
        #Insert the random code into the database
        roux.execute(f"INSERT INTO `pussybot_verification` (`discord_id`, `code`) VALUES ({member.id}, {random_code});")
        xd.commit()
        
        #DM the user the code
        try: 
            await member.send(f"Hello, {member.mention}!\nPlease use this code to verify that you are not a bot: `{random_code}`\n\n**This code will only work for you**")
        except:
            await channel.send(f"{member.mention}! Your DMs are disabled, please enable them and rejoin the server to receive your verification code.")
            pass
        
        embed = discord.Embed(title=f"{member.name} joined", description=f"{member.mention}, please check your DMs for a code and paste it in the verify channel to continue. If you have not received a DM, turn them on and rejoin.", timestamp=datetime.datetime.utcnow(), color=discord.Color.default())
        await channel.send(embed=embed)
        
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = bot.get_channel(985674998956060732)
        embed = discord.Embed(title=f"{member.name} left", description=f"{member.mention} has left the server.", timestamp=datetime.datetime.utcnow(), color=discord.Color.default())
        await channel.send(embed=embed)
        

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        try:
            embed = discord.Embed(title=f"Message deleted", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.add_field(name="Author", value=f"{message.author} [{message.author.id}]", inline=True)
            embed.add_field(name="Content", value=message.content, inline=True)
            if 'http' in message.content:
                if 'https' in message.content: url = re.findall(r'(https?://[^\s]+)', message.content)
                else: url = re.findall(r'(http?://[^\s]+)', message.content)
                embed.add_field(name="Link(s)", value=f"{url}", inline=True)
            
            await bot.get_channel(939685647025848380).send(embed=embed)
        except:
            embed = discord.Embed(title=f"Message deleted", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.add_field(name="Author", value=f"{message.author} [{message.author.id}]", inline=True)
            embed.add_field(name="Content", value="Most likely an embed or attachment", inline=True)

            if message.attachments:
                if len(message.attachments) == 1:
                    embed.add_field(name="Attachment", value=message.attachments[0].url)
                    if message.attachments[0].url.endswith(('.jpg', '.png', '.jpeg', '.gif')): 
                        extension = message.attachments[0].url.split(".")[-1]

                        img_data = requests.get(message.attachments[0].url).content
                        with open(f'attachments/{message.id}.{extension}', 'wb') as handler: handler.write(img_data)
                        file = discord.File(f"attachments/{str(message.id)}.{str(extension)}", filename=f"image.{extension}")
                        embed.set_image(url=f"attachment://image.{extension}")
            
            try:
                await bot.get_channel(939685647025848380).send(file=file, embed=embed)
                os.remove(f"attachments/{message.id}.{extension}")
            except:
                return
                
                

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == bot.user.id: return
        
        if message.channel.id == 983381315804069989:  
            xd.reconnect(attempts=3)
            roux.execute(f"SELECT * FROM `pussybot_verification` WHERE `discord_id` = {message.author.id}")
            result = roux.fetchall()
            
            for i in result:
                discord_id = str(i).split(", ")[0].replace("(", "")
                code = str(i).split(", ")[1].replace(")", "")
                if message.content == code and message.author.id == int(discord_id):
                    #Delete the code from the database
                    roux.execute(f"DELETE FROM `pussybot_verification` WHERE `discord_id` = {discord_id} AND `code` = {code}")
                    xd.commit()
                    
                    #DM the user that they are verified, and remove the role
                    await message.author.send(f"You have been verified, welcome to the server!")
                    await message.author.add_roles(message.author.guild.get_role(983382374006005840))
                    
                    #Send a message to the new users channel that the user has been verified
                    embed = discord.Embed(title=f"✅ {message.author.name} has been verified", description=f"{message.author.mention} ({message.author.id})", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
                    await bot.get_channel(983392113746141204).send(embed=embed)
                    
        if message.channel.id == 985325859235835915:
            embed = discord.Embed(title=f"Anonymous confession", description=f"{message.content}", timestamp=datetime.datetime.utcnow(), color=discord.Color.default())

            if message.attachments:
                if len(message.attachments) == 1:
                    embed.add_field(name="Attachment", value=message.attachments[0].url)
                    if message.attachments[0].url.endswith(('.jpg', '.png', '.jpeg', '.gif')): 
                        extension = message.attachments[0].url.split(".")[-1]

                        img_data = requests.get(message.attachments[0].url).content
                        with open(f'attachments/{message.id}.{extension}', 'wb') as handler: handler.write(img_data)
                        file = discord.File(f"attachments/{str(message.id)}.{str(extension)}", filename=f"image.{extension}")
                        embed.set_image(url=f"attachment://image.{extension}")

                        await bot.get_channel(943677015486267482).send(file=file, embed=embed)
                        await message.delete()
                        return
            
            
            await bot.get_channel(943677015486267482).send(embed=embed)
            await message.delete()
        
        #Automod
        if cbx.is_connected(): pass
        else: cbx.reconnect(attempts=3)
        
        csr.execute("SELECT * FROM `RestrictedWords`")
        result = csr.fetchall()
        for i in result:
            if i[0] in message.content.lower():
                await message.delete()
                try:
                    await message.author.send(f"You have used a restricted word, please do not use `{i[0]}` in your messages.")
                except:
                    await message.channel.send(f"{message.author.mention} has used a restricted word, please do not use `{i[0]}` in your messages.")
                return        
           
        if message.author.bot: return
        if message.guild is None: return

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        try:
            if message_before.content == message_after.content: return
            embed=discord.Embed(title=f"Message edited (click to view)", url=f"https://discord.com/channels/{message_before.guild.id}/{message_before.channel.id}/{message_before.id}", timestamp=datetime.datetime.utcnow(), color=0xFFFF00)
            embed.add_field(name="Author", value=f"{message_before.author} [{message_before.author.id}]", inline=True)
            embed.add_field(name="Before", value=message_before.content, inline=True)
            embed.add_field(name="After", value=message_after.content, inline=True)
                
            if message_before.attachments:
                if len(message_before.attachments) == 1:
                    embed.add_field(name="Attachment", value=message_before.attachments[0].url)
                    if message_before.attachments[0].url.endswith(('.jpg', '.png', '.jpeg', '.gif')): 
                        
                        extension = message_before.attachments[0].url.split(".")[-1]

                        img_data = requests.get(message_before.attachments[0].url).content
                        with open(f'attachments/{message_before.id}.{extension}', 'wb') as handler:
                            handler.write(img_data)
                        file = discord.File("attachments/" + str(message_before.id) + "." + str(extension), filename=f"image.{extension}")
                        embed.set_image(url=f"attachment://image.{extension}")
                
            try:
                await bot.get_channel(939685647025848380).send(file=file, embed=embed)
            except: 
                await bot.get_channel(939685647025848380).send(embed=embed)
        except:
            embed=discord.Embed(title=f"Message edited (click to view)", url=f"https://discord.com/channels/{message_before.guild.id}/{message_before.channel.id}/{message_before.id}", timestamp=datetime.datetime.utcnow(), color=0xFFFF00)
            embed.add_field(name="Author", value=f"{message_before.author} [{message_before.author.id}]", inline=True)
            embed.add_field(name="Before", value="Most likely an embed or attachment", inline=True)
            embed.add_field(name="After", value=message_after.content, inline=True)
            if message_before.attachments:
                if len(message_before.attachments) == 1:
                    embed.add_field(name="Attachment", value=message_before.attachments[0].url)
                    if message_before.attachments[0].url.endswith(('.jpg', '.png', '.jpeg', '.gif')): #Find the extension, if not supported, crashes. Oops
                        
                        extension = message_before.attachments[0].url.split(".")[-1]

                        img_data = requests.get(message_before.attachments[0].url).content
                        with open(f'attachments/{message_before.id}.{extension}', 'wb') as handler:
                            handler.write(img_data)
                        file = discord.File("attachments/" + str(message_before.id) + "." + str(extension), filename=f"image.{extension}")
                        embed.set_image(url=f"attachment://image.{extension}")
                
            try:
                await bot.get_channel(939685647025848380).send(file=file, embed=embed)
            except:
                try:
                    await bot.get_channel(939685647025848380).send(embed=embed)
                except:
                    embed=discord.Embed(title=f"CRITICAL ERROR", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
                    embed.add_field(name="What caused this?", value="Either a bug in Discord, or a bug in pussybot's code.", inline=True)
                    embed.add_field(name="How to fix?", value="tell gravy", inline=True)
                    embed.add_field(name="Author", value=f"{message_before.author} [{message_before.author.id}]", inline=True)
                    await bot.get_channel(939685647025848380).send(embed=embed)
                    
                    
    # @commands.Cog.listener()
    # async def on_reaction_added(self, reaction, user):
        
        


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        #if isinstance(error, commands.CommandNotFound):  return
        if isinstance(error, commands.errors.DisabledCommand): return
        if isinstance(error, commands.errors.CommandOnCooldown): 
            a = int(error.retry_after)
            await ctx.send(embed=discord.Embed(title="Cooldown", description=f"{ctx.author.name}, You are on cooldown for {str(a)} seconds."))
            return
        if isinstance(error, commands.errors.CommandNotFound): return
        if hasattr(ctx.command, "on_error"): return
            
        error = getattr(error, "original", error)
        em = discord.Embed(title="Error", description=str(error).capitalize(), color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
        await ctx.send(embed=em, delete_after=5.0)
        
    

        
def setup(bot): bot.add_cog(Events(bot))
print(c.color.GREEN + "Events cog loaded" + c.color.END)