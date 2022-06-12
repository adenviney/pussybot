import asyncio,discord,random, mysql.connector, json
from discord.ext import commands

with open('./ext/database-conf2.json') as f:
    config = json.load(f)

try: #Everything
    cnxm = mysql.connector.connect(**config)
    cursor = cnxm.cursor()
    print(f"Connected to {config['user']}")
except mysql.connector.Error as err: #This is fine
    print("You fucked up lmao" + err)
print("Loaded levelling database successfully")

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def genXP(self, amt, boost): 
        coolroblox = 0
        if amt >= 100:  coolroblox = random.randint(1, 100)
        elif amt >= 50: coolroblox = random.randint(1, 50)
        else: coolroblox = random.randint(1, 25)
        
        if boost: coolroblox = coolroblox * 2
            
        return coolroblox
        
        
    @commands.command(name="setlevel", brief="Set the level of a user")
    @commands.has_permissions(administrator=True)
    async def setlevel(self, ctx, user: discord.Member, level: int):
        eas = False
        if cnxm.is_connected(): pass
        else: cnxm.reconnect(attempts=3)
        if level is None: level = 69
        if level > 690000:
            await ctx.reply(f"{ctx.author.name}, you cannot set a level higher than 690000")
            return
        if level < 0:
            eas = True
        cursor.execute("UPDATE `" + str(ctx.guild.id) + "` SET UserXP = " + str(level * 1000) + ", UserLevel = " + str(level) + " WHERE ClientID = " + str(user.id) + ";")
        cnxm.commit()
        if eas: 
            await ctx.reply(f"{user.mention}'s level has been set to {level}, what did they do to deserve this?")
        else:
            await ctx.reply(f"{user.mention}'s level has been set to {level}")
 
        
    @commands.command(aliases=['lb'], name="leaderboard", brief="Get the top X levels in the server")
    async def leaderboard(self, ctx, amt: int = 10):
        await asyncio.sleep(0.2)
        try:
            cursor.execute("SELECT UserLevel, ClientID FROM `" + str(ctx.guild.id) + f"` ORDER BY UserLevel * 1 DESC LIMIT {amt};")
        except Exception as e:
            await ctx.reply(f"There aren't that many users in the database yet, please lower the amount {e}")
            return
        
        desc = []
        for i, pos in enumerate(cursor.fetchall()):
            lvl, memberID = pos
            guild = ctx.guild
            member = guild.get_member(memberID)
            if member is None: 
                #Remove from database
                cursor.execute("DELETE FROM `" + str(ctx.guild.id) + "` WHERE ClientID = " + str(memberID) + ";")
                member = "Unknown member (ID: " + str(memberID) + ")"
            desc.append(f"{i+1}. {member} - {lvl}")
            
        embed = discord.Embed(title=f"Top {amt} levels in {ctx.guild.name}", description="\n".join(desc), color=0x885DD3)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['userlevel', 'userlvl', 'lvl'], brief="Get your (or someone else's) user level")
    async def level(self, ctx, *, user: discord.Member = None):
        await asyncio.sleep(0.2)
        if user is None: 
            ID = ctx.author.id
        else: 
            ID = user.id
        cursor.execute("SELECT UserXP, UserLevel FROM `" + str(ctx.guild.id) + "` WHERE ClientID = " + str(ID) + ";")
        result = cursor.fetchall()
        if len(result) == 0:
            if ID == ctx.author.id: 
                embed = discord.Embed(title="No records found :(", description=f"You have no level yet, start typing in this server to gain experience!", color=0x885DD3)
                embed.set_thumbnail(url=ctx.author.avatar)
                await ctx.reply(embed=embed)
            else: 
                embed = discord.Embed(title="No records found :(", description=f"{user.mention} has no level yet, they start typing in this server to gain experience!", color=0x885DD3)
                embed.set_thumbnail(url=ctx.author.avatar)
                await ctx.reply(embed=embed)
        else:
            newXP = result[0][0]
            currentLevel = int(newXP / 1000)
            if currentLevel == 0: currentLevel = 1
            if ID == ctx.author.id:
                embed = discord.Embed(title=f"{ctx.author.name}'s level", description=f"You are currently level {str(currentLevel)} with {str(newXP)} experience", color=0x885DD3)
                embed.set_thumbnail(url=ctx.author.avatar)
                if "xp-spam" in ctx.channel.name:
                    embed.set_footer(text="You're getting x2 XP for xp-spam being in the channel name!")
                else:
                    embed.set_footer(text=f"Tip: Trying to get more XP? Create a channel with \"xp-spam\" in the name for a x2 XP boost!")
                await ctx.reply(embed=embed)
            else:
                embed = discord.Embed(title=f"{user.name}'s level", description=f"{user.mention} is currently level {str(currentLevel)} with {str(newXP)} experience", color=0x885DD3)
                embed.set_thumbnail(url=user.avatar)
                await ctx.reply(embed=embed)
            
    @commands.Cog.listener()
    @commands.has_permissions(send_messages=True)
    async def on_message(self, message):
        if message.author.bot: return
        if message.guild is None: return
        
        if cnxm.is_connected(): pass
        else: cnxm.reconnect(attempts=3)
        
        try:
            cursor.execute("SELECT UserXP, UserLevel FROM `" + str(message.guild.id) + "` WHERE ClientID = " + str(message.author.id) + ";")
        except:
            cursor.execute("CREATE TABLE `" + str(message.guild.id) + "`(ClientID BIGINT NOT NULL PRIMARY KEY, UserXP INT NOT NULL DEFAULT 0, UserLevel INT NOT NULL DEFAULT 0);")
            cnxm.commit()
            cursor.execute("SELECT UserXP, UserLevel FROM `" + str(message.guild.id) + "` WHERE ClientID = " + str(message.author.id) + ";")
        
        if "xp-spam" in message.channel.name:
            xp = self.genXP(int(len(message.content)), True)
        else:
            xp = self.genXP(int(len(message.content)), False)
        result = cursor.fetchall()
        if len(result) == 0:
            cursor.execute("INSERT INTO `" + str(message.guild.id) + "` VALUES(" + str(message.author.id) + "," + str(xp) + ", 1);")
            cnxm.commit()
        else:
            newXP = result[0][0] + xp
            oldLevel = result[0][1]
            flag = False
            currentLevel = int(newXP / 1000)
            if currentLevel > oldLevel: flag = True
            if currentLevel == 0: currentLevel = 1
            cursor.execute("UPDATE `" + str(message.guild.id) + "` SET UserXP = " + str(newXP) + ", UserLevel = " + str(currentLevel) + " WHERE ClientID = " + str(message.author.id) + ";")
            cnxm.commit()
            
            if flag:
                embed = discord.Embed(title="Level Up!", description=f"{message.author.mention} has leveled up to level {currentLevel}!", color=0x885DD3)
                embed.set_thumbnail(url=message.author.avatar)
                await message.channel.send(embed=embed)

def setup(bot): bot.add_cog(Leveling(bot))
print("Leveling cog loaded")