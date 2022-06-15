import datetime, discord, requests, re, random, os, lib.AI as AI, lib.database as db
from discord.ext import commands, tasks
from pussybot import bot, VERSION

xd, roux = db.db.connect("db3")
cbx, csr = db.db.connect("db4")
connect, cursor = db.db.connect("db5")

class Events(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot
        self.version = VERSION
        self.max_window = 5
        self.window_time_ms = 5000
        self.stockloop.start()
    
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
        
        if message.channel.id == 986085778625032192:
            if message.author.id == bot.user.id: return
            if message.content.startswith("#"): return
            #Call AI API
            resp = AI.ask(message.content)
            await message.channel.send(embed=discord.Embed(title="Response", description=resp, color=0x36393F))
        
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
        
    @tasks.loop(seconds=10)
    async def stockloop(self):
        if connect.is_connected(): pass
        else: connect.reconnect(attempts=3)
        
        #Randomly change stock prices up or down to simulate market movement
        cursor.execute("SELECT * FROM stocks")
        result = cursor.fetchall()
        for i in result:
            minus_or_plus = random.choice(["-", "+"])
            spike = random.choice([200, 300, 1000, 20, 70, 2000])
            #Stop stocks from going below 0
            if i[0] <= 200: minus_or_plus = "+"
            
            if minus_or_plus == "-": change_rate = f"▼ {str((i[0] - spike) / i[0])[:4]}"
            elif minus_or_plus == "+": change_rate = f"▲ {str((i[0] + spike) / i[0])[:4]}"
                
            cursor.execute(f"UPDATE stocks SET price = price {minus_or_plus} {random.randint(1, spike)} WHERE name = '{i[1]}'")
            cursor.execute(f"UPDATE stocks SET change_rate = '{change_rate}' WHERE name = '{i[1]}'")
            connect.commit()
                
            


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        #if isinstance(error, commands.CommandNotFound):  return
        if isinstance(error, commands.errors.DisabledCommand): return
        if isinstance(error, commands.errors.CommandNotFound): return
        if isinstance(error, commands.errors.CommandOnCooldown): 
            a = int(error.retry_after)
            #convert a into hours, minutes, seconds
            months = a // 2678400
            weeks = a // 604800
            days = a // 86400
            hours = a // 3600
            minutes = (a % 3600) // 60
            seconds = (a % 3600) % 60
            #Add them all up into one string 
            if months > 0: time = f"{months} more months"
            elif weeks > 0: time = f"{weeks} more weeks"
            elif days > 0: time = f"{days} more days"
            elif hours > 0: time = f"{hours} more hours"
            elif minutes > 0: time = f"{minutes} more minute(s)"
            elif seconds > 0: time = f"{seconds} more seconds"
            await ctx.send(embed=discord.Embed(title="Woah, slow it down there", description=f"{ctx.author.name}, you are on cooldown for {str(time)}."))
            return
        if hasattr(ctx.command, "on_error"): return
            
        error = getattr(error, "original", error)
        em = discord.Embed(title="Error", description=str(error).capitalize(), color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
        await ctx.send(embed=em, delete_after=5.0)

def setup(bot): bot.add_cog(Events(bot))