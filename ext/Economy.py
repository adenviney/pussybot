from ast import alias
import discord, lib.color as c, mysql.connector, random, json
from discord.ext import commands

with open('./json/database-conf5.json') as f: 
    config = json.load(f)

try: #Everything
    connect = mysql.connector.connect(**config)
    cursor = connect.cursor()
except mysql.connector.Error as err: 
    print(c.color.FAIL + "[ERROR] " + c.color.END + str(err))

def addcomma(amount): 
    return ("{:,}".format(amount))
class Economy(commands.Cog):    
    def __init__(self, bot): 
        self.bot = bot
        
    #Commands: $invest, $buy, $sell, $work, $shop, $inventory, $use, $stats, $daily, $weekly, $monthly, $yearly, $economy
        
    @commands.command(name="beg", brief="Beg for coins")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self, ctx):
        #Randomly pick wether they agree to give them money or not
        if random.randint(1, 5) == 1: 
            no = random.choice(["What? Give YOU money? Hahahaha no.", 
                                "I got bills to pay man",
                                "I don't have any money...", 
                                "Go beg somewhere else bozo",
                                "You're not worth it",
                                "Your acting is horrible",
                                "You're not my time",
                                "Move it",
                                "In your dreams",
                                "Who said that? *quickly runs away*"])
            
            await ctx.send(embed=discord.Embed(title=no, color=discord.Color.red()))
            return
        
        amount = random.randint(10, 100)
        if connect.is_connected(): pass
        else: connect.reconnect(attempts=3)
        #Check if user is in database
        cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
        if cursor.fetchone() is None:
            cursor.execute(f"INSERT INTO users (id, coins, bank) VALUES ({str(ctx.author.id)}, {str(amount)}, {str(0)});")
            connect.commit()
        else:  
            cursor.execute(f"UPDATE users SET coins = coins + {str(amount)} WHERE id = {str(ctx.author.id)}")
            connect.commit()
        embed = discord.Embed(title=f"You were given `${amount}` coins for begging.", color=discord.Color.green())
        embed.set_footer(text="What a begger you are.")
        await ctx.send(embed=embed)
        
    @commands.command(name="deposit", brief="Deposit coins", aliases=["dep"])
    async def deposit(self, ctx, amount: str = 0):
        if connect.is_connected(): pass
        else: connect.reconnect(attempts=3)
        try:
            if int(amount) == 0:
                await ctx.send(embed=discord.Embed(title="Please specify an amount of coins to deposit.", color=discord.Color.red()))
                return
            
        except:
            if str(amount) == "all":
                cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
                if cursor.fetchone() is None:
                    await ctx.send(embed=discord.Embed(title="You don't have any coins to deposit.", color=discord.Color.red()))
                    return
                
                cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
                coins = cursor.fetchone()[0]
                amount = coins
                
        amount = int(amount)
        
        if amount < 0:
            await ctx.send(embed=discord.Embed(title="Please specify a positive amount of coins to deposit.", color=discord.Color.red()))
            return
        
        cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
        if cursor.fetchone() is None:
            await ctx.send(embed=discord.Embed(title="You don't have any coins to deposit. Try begging for some coins", color=discord.Color.red()))
            return
        
        cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
        if cursor.fetchone()[0] < amount:
            await ctx.send(embed=discord.Embed(title="You don't have enough coins to deposit.", color=discord.Color.red()))
            return
        
        cursor.execute(f"UPDATE users SET coins = coins - {str(amount)} WHERE id = {str(ctx.author.id)}")
        cursor.execute(f"UPDATE users SET bank = bank + {str(amount)} WHERE id = {str(ctx.author.id)}")
        connect.commit()
        await ctx.send(embed=discord.Embed(title=f"You deposited `${addcomma(amount)}` coins.", color=discord.Color.green()))
        
    @commands.command(name="withdraw", brief="Withdraw coins", aliases=["with"])
    async def withdraw(self, ctx, amount: str = 0):
        if connect.is_connected(): pass
        else: connect.reconnect(attempts=3)
        try:
            if int(amount) == 0:
                await ctx.send(embed=discord.Embed(title="Please specify an amount of coins to deposit.", color=discord.Color.red()))
                return
            
        except:
            if str(amount) == "all":
                cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
                if cursor.fetchone() is None:
                    await ctx.send(embed=discord.Embed(title="You don't have any coins to withdraw.", color=discord.Color.red()))
                    return
                
                cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
                coins = cursor.fetchone()[2]
                amount = coins
                
        amount = int(amount)
        
        if amount < 0:
            await ctx.send(embed=discord.Embed(title="Please specify a positive amount of coins to withdraw.", color=discord.Color.red()))
            return
        
        cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
        if cursor.fetchone() is None:
            await ctx.send(embed=discord.Embed(title="You don't have any coins to withdraw. Try depositing some coins", color=discord.Color.red()))
            return
        
        cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
        if cursor.fetchone()[2] < amount:
            await ctx.send(embed=discord.Embed(title="You don't have enough coins to withdraw.", color=discord.Color.red()))
            return
        
        cursor.execute(f"UPDATE users SET coins = coins + {str(amount)} WHERE id = {str(ctx.author.id)}")
        cursor.execute(f"UPDATE users SET bank = bank - {str(amount)} WHERE id = {str(ctx.author.id)}")
        connect.commit()
        await ctx.send(embed=discord.Embed(title=f"You withdrew `${addcomma(amount)}` coins.", color=discord.Color.green()))
        
    @commands.command(name="balance", brief="Check your balance", aliases=["bal"])
    async def bal(self, ctx, user: discord.Member = None):
        if connect.is_connected(): pass
        else: connect.reconnect(attempts=3)
        
        if user is None:
            #Get coins from wallet and display bank balance
            cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
            if cursor.fetchone() is None:
                await ctx.send(embed=discord.Embed(title="You have no coins in your wallet or bank. Broke ass", color=discord.Color.red()))
                return
            
            cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
            coins = cursor.fetchone()[0]
            cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
            bank = cursor.fetchone()[2]
            embed = discord.Embed(title="Balance", description=f"**Wallet:** `${addcomma(coins)}`\n**Bank:** `${addcomma(bank)}`", color=discord.Color.green())
            await ctx.send(embed=embed)
            connect.commit()
            return
        else: 
            #Get coins from wallet and display bank balance
            cursor.execute(f"SELECT * FROM users WHERE id = {str(user.id)};")
            if cursor.fetchone() is None:
                await ctx.send(embed=discord.Embed(title="This user has no coins in their wallet or bank. Broke ass", color=discord.Color.red()))
                return
            
            cursor.execute(f"SELECT * FROM users WHERE id = {str(user.id)};")
            coins = cursor.fetchone()[0]
            cursor.execute(f"SELECT * FROM users WHERE id = {str(user.id)};")
            bank = cursor.fetchone()[2]
            embed = discord.Embed(title=f"{user.name}#{user.discriminator}'s Balance", description=f"**Wallet:** `${addcomma(coins)}`\n**Bank:** `${addcomma(bank)}`", color=discord.Color.green())
            await ctx.send(embed=embed)
            connect.commit()
            return
        
    @commands.command(name="pay", brief="Pay someone", aliases=["give"])
    async def pay(self, ctx, user: discord.Member, amount: str = 0):
        if user.id == ctx.author.id:
            await ctx.send(embed=discord.Embed(title="You can't pay yourself. Bruh.", color=discord.Color.red()))
            return
        
        if connect.is_connected(): pass
        else: connect.reconnect(attempts=3)
        try:
            if int(amount) == 0:
                await ctx.send(embed=discord.Embed(title="Please specify an amount of coins to pay.", color=discord.Color.red()))
                return
            
        except:
            if str(amount) == "all":
                cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
                if cursor.fetchone() is None:
                    await ctx.send(embed=discord.Embed(title="You don't have any coins to pay.", color=discord.Color.red()))
                    return
                
                cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
                coins = cursor.fetchone()[0]
                amount = coins
                amount = int(amount)
                tax = round(amount / 100) #Taxes user. If user was to give $900,000, they would be taxed $9,000.
                amount = (amount - tax) #Removes total for tax
                amount = (amount + tax) #Adds tax on

        amount = int(amount)

        try:
            if tax >= 1: pass
        except:
            tax = round(amount / 100) #Taxes user. If user was to give $900,000, they would be taxed $9,000.
            amount = (amount + tax) #Adds tax to amount
            
        
        if amount < 0:
            await ctx.send(embed=discord.Embed(title="Please specify a positive amount of coins to pay.", color=discord.Color.red()))
            return
        
        cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
        if cursor.fetchone() is None:
            await ctx.send(embed=discord.Embed(title="You don't have any coins to pay. Try depositing some coins", color=discord.Color.red()))
            return
        
        cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
        if cursor.fetchone()[0] < amount:
            await ctx.send(embed=discord.Embed(title=f"You don't have enough coins to pay. `${addcomma(amount - tax)}` (+ `{tax}` tax)", color=discord.Color.red()))
            return
        
        cursor.execute(f"SELECT * FROM users WHERE id = {str(user.id)};")
        if cursor.fetchone() is None:
            cursor.execute(f"INSERT INTO users (id, coins, bank) VALUES ({str(user.id)}, {str(0)}, {str(0)});")
        
        
        cursor.execute(f"UPDATE users SET coins = coins - {str(amount)} WHERE id = {str(ctx.author.id)}")
        cursor.execute(f"UPDATE users SET coins = coins + {str(amount - tax)} WHERE id = {str(user.id)}")
        connect.commit()
        embed=discord.Embed(title=f"You paid {user.name}", color=discord.Color.green())
        embed.add_field(name="Amount", value=f"`${addcomma(amount - tax)}`", inline=True)
        embed.add_field(name="Tax", value=f"`${addcomma(tax)}`", inline=True)
        embed.add_field(name="Total", value=f"`${addcomma(amount)}`", inline=True)
        await ctx.send(embed=embed)
        
    @commands.command(name="work", brief="Work for money", aliases=["labour"])
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def work(self, ctx):
        if connect.is_connected(): pass
        else: connect.reconnect(attempts=3)
        
        how_good_did_I_work = random.randint(1, 100)
        pay = 45000
        
        if how_good_did_I_work <= 25:
            await ctx.send(embed=discord.Embed(title="You didn't work hard enough. You weren't payed.", color=discord.Color.red()))
            return
        elif how_good_did_I_work <= 50:
            pay = (pay / 2)
            await ctx.send(embed=discord.Embed(title=f"You worked decently, your pay was split in half: `${addcomma(pay)}`", color=discord.Color.gold()))
            cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
            if cursor.fetchone() is None:
                cursor.execute(f"INSERT INTO users (id, coins, bank) VALUES ({str(ctx.author.id)}, {str(0)}, {str(pay)});")
                return
            
            cursor.execute(f"UPDATE users SET bank = bank + {str(pay)} WHERE id = {str(ctx.author.id)}")
            connect.commit()
            return
        elif how_good_did_I_work <= 75:
            await ctx.send(embed=discord.Embed(title=f"You worked hard, you got full pay: `${addcomma(pay)}`", color=discord.Color.green()))
            cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
            if cursor.fetchone() is None:
                cursor.execute(f"INSERT INTO users (id, coins, bank) VALUES ({str(ctx.author.id)}, {str(0)}, {str(pay)});")
                return
            
            cursor.execute(f"UPDATE users SET bank = bank + {str(pay)} WHERE id = {str(ctx.author.id)}")
            connect.commit()
            return
        elif how_good_did_I_work <= 90:
            pay = (pay + random.randint(1, 100000))
            await ctx.send(embed=discord.Embed(title=f"You worked really hard, you got a bonus: `${addcomma(pay)}`", color=discord.Color.blue()))
            cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
            if cursor.fetchone() is None:
                cursor.execute(f"INSERT INTO users (id, coins, bank) VALUES ({str(ctx.author.id)}, {str(0)}, {str(pay)});")
                return
            
            cursor.execute(f"UPDATE users SET bank = bank + {str(pay)} WHERE id = {str(ctx.author.id)}")
            connect.commit()
            return
            
        
            
    
    
def setup(bot): bot.add_cog(Economy(bot))
print(c.color.GREEN + "Economy cog loaded" + c.color.END)