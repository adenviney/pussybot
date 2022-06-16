import discord, random, lib.database as db, discord.ui, lib.constants as const
from discord.ext import commands

connect, cursor = db.db.connect("db5")

def addcomma(amount): 
    return ("{:,}".format(amount))

cards = const.load.cards

class viewstuff(discord.ui.View): 
    
    # def __init__(self, ctx, player_cards, dealer_cards):
    #     self.ctx = ctx
    
    def __init__(self, ctx, player_cards, dealer_cards, bet, wallet):
        super().__init__(timeout=20)
        self.ctx = ctx
        self.player_cards = player_cards
        self.dealer_cards = dealer_cards
        self.bet = bet
        self.wallet = wallet
    
        
    @discord.ui.button(label="Hit", style=discord.ButtonStyle.blurple)
    async def hit_callback(self, button, interaction):
        if interaction.user.id == self.ctx.author.id:
            self.clear_items()
            self.player_cards.append(random.choice(cards))
            self.dealer_cards.append(random.choice(cards))
            self.dealer_cards.append(random.choice(cards))
            
            #Add up the total of the players cards
            player_total = 0
            for card in self.player_cards:
                if card == "J" or card == "Q" or card == "K":
                    player_total += 10
                elif card == "A":
                    if player_total + 11 > 21:
                        player_total += 1
                    else:
                        player_total += 11
                else:
                    player_total += int(card)
                    
            #Add up the total of the dealers cards
            dealer_total = 0
            for card in self.dealer_cards:
                if card == "J" or card == "Q" or card == "K":
                    dealer_total += 10
                elif card == "A":
                    if dealer_total + 11 > 21:
                        dealer_total += 1
                    else:
                        dealer_total += 11
                else:
                    dealer_total += int(card)
                    
            #Check if the player has blackjack
            if player_total == 21:
                embed = discord.Embed(title="Blackjack", description=f"You won `${addcomma(self.bet)}`!", color=discord.Color.green())
                embed.add_field(name="You", value=f"`{self.player_cards[0]}` `{self.player_cards[1]}` `{self.player_cards[2]}`\nTotal: {player_total}", inline=True)
                embed.add_field(name="Dealer", value=f"`{self.dealer_cards[0]}` `{self.dealer_cards[1]}` `{self.dealer_cards[2]}`\nTotal: {dealer_total}", inline=True)
                await interaction.response.edit_message(embed=embed, view=self)
                cursor.execute(f"UPDATE users SET coins = coins + {addcomma(self.bet)} WHERE id = {str(self.ctx.author.id)};")
                return
            if player_total > 21:
                embed = discord.Embed(title="Blackjack", description=f"You lost :(\nYou lost `${addcomma(self.bet)}`", color=discord.Color.red())
                embed.add_field(name="You", value=f"`{self.player_cards[0]}` `{self.player_cards[1]}` `{self.player_cards[2]}`\nTotal: {player_total}", inline=True)
                embed.add_field(name="Dealer", value=f"`{self.dealer_cards[0]}` `{self.dealer_cards[1]}` `{self.dealer_cards[2]}`\nTotal: {dealer_total}", inline=True)
                await interaction.response.edit_message(embed=embed, view=self)
                cursor.execute(f"UPDATE users SET coins = coins - {addcomma(self.bet)} WHERE id = {str(self.ctx.author.id)};")
                return
            if player_total > dealer_total:
                embed = discord.Embed(title="Blackjack", description=f"You won `${addcomma(self.bet)}`!", color=discord.Color.green())
                embed.add_field(name="You", value=f"`{self.player_cards[0]}` `{self.player_cards[1]}` `{self.player_cards[2]}`\nTotal: {player_total}", inline=True)
                embed.add_field(name="Dealer", value=f"`{self.dealer_cards[0]}` `{self.dealer_cards[1]}` `{self.dealer_cards[2]}`\nTotal: {dealer_total}", inline=True)
                await interaction.response.edit_message(embed=embed, view=self)
                cursor.execute(f"UPDATE users SET coins = coins + {addcomma(self.bet)} WHERE id = {str(self.ctx.author.id)};")
                return
            if dealer_total > 21:
                embed = discord.Embed(title="Blackjack", description=f"You won `${addcomma(self.bet)}`!", color=discord.Color.green())
                embed.add_field(name="You", value=f"`{self.player_cards[0]}` `{self.player_cards[1]}` `{self.player_cards[2]}`\nTotal: {player_total}", inline=True)
                embed.add_field(name="Dealer", value=f"`{self.dealer_cards[0]}` `{self.dealer_cards[1]}` `{self.dealer_cards[2]}`\nTotal: {dealer_total}", inline=True)
                await interaction.response.edit_message(embed=embed, view=self)
                cursor.execute(f"UPDATE users SET coins = coins + {addcomma(self.bet)} WHERE id = {str(self.ctx.author.id)};")
                return
            if player_total < dealer_total:
                embed = discord.Embed(title="Blackjack", description=f"You lost :(\nYou lost `${addcomma(self.bet)}`", color=discord.Color.red())
                embed.add_field(name="You", value=f"`{self.player_cards[0]}` `{self.player_cards[1]}` `{self.player_cards[2]}`\nTotal: {player_total}", inline=True)
                embed.add_field(name="Dealer", value=f"`{self.dealer_cards[0]}` `{self.dealer_cards[1]}` `{self.dealer_cards[2]}`\nTotal: {dealer_total}", inline=True)
                await interaction.response.edit_message(embed=embed, view=self)
                cursor.execute(f"UPDATE users SET coins = coins - {addcomma(self.bet)} WHERE id = {str(self.ctx.author.id)};")
                return
            if player_total == dealer_total:
                embed = discord.Embed(title="Blackjack", description="Tie!\nYou didn't loose any money", color=discord.Color.gold())
                embed.add_field(name="You", value=f"`{self.player_cards[0]}` `{self.player_cards[1]}` `{self.player_cards[2]}`\nTotal: {player_total}", inline=True)
                embed.add_field(name="Dealer", value=f"`{self.dealer_cards[0]}` `{self.dealer_cards[1]}` `{self.dealer_cards[2]}`\nTotal: {dealer_total}", inline=True)
                await interaction.response.edit_message(embed=embed, view=self)
                return
        else:
            await interaction.response.send_message(f"{interaction.user.name}, you cannot play someone else's game.", ephemeral=True)
            return
        
    @discord.ui.button(label="Stand", style=discord.ButtonStyle.blurple)
    async def stand_callback(self, button, interaction):
        if interaction.user.id == self.ctx.author.id:
            self.clear_items()
            self.dealer_cards.append(random.choice(cards))
            self.dealer_cards.append(random.choice(cards))
            
            #Add up the total of the dealers cards
            dealer_total = 0
            for card in self.dealer_cards:
                if card == "J" or card == "Q" or card == "K":
                    dealer_total += 10
                elif card == "A":
                    if dealer_total + 11 > 21:
                        dealer_total += 1
                    else:
                        dealer_total += 11
                else:
                    dealer_total += int(card)
                    
            player_total = 0
            for card in self.player_cards:
                if card == "J" or card == "Q" or card == "K":
                    player_total += 10
                elif card == "A":
                    if player_total + 11 > 21:
                        player_total += 1
                    else:
                        player_total += 11
                else:
                    player_total += int(card)
                    
            #Check if the dealer has blackjack
            if dealer_total == 21:
                embed = discord.Embed(title="Blackjack", description=f"You lost :(\nYou lost `${addcomma(self.bet)}`", color=discord.Color.red())
                embed.add_field(name="You", value=f"`{self.player_cards[0]}` `{self.player_cards[1]}`\nTotal: {player_total}", inline=True)
                embed.add_field(name="Dealer", value=f"`{self.dealer_cards[0]}` `{self.dealer_cards[1]}` `{self.dealer_cards[2]}`\nTotal: {dealer_total}", inline=True)
                await interaction.response.edit_message(embed=embed, view=self)
                cursor.execute(f"UPDATE users SET coins = coins - {addcomma(self.bet)} WHERE id = {str(self.ctx.author.id)};")
                return
            if player_total > 21: 
                embed = discord.Embed(title="Blackjack", description=f"You lost :(\nYou lost `${addcomma(self.bet)}`", color=discord.Color.red())
                embed.add_field(name="You", value=f"`{self.player_cards[0]}` `{self.player_cards[1]}` `{self.player_cards[2]}`\nTotal: {player_total}", inline=True)
                embed.add_field(name="Dealer", value=f"`{self.dealer_cards[0]}` `{self.dealer_cards[1]}` `{self.dealer_cards[2]}`\nTotal: {dealer_total}", inline=True)
                await interaction.response.edit_message(embed=embed, view=self)
                cursor.execute(f"UPDATE users SET coins = coins - {addcomma(self.bet)} WHERE id = {str(self.ctx.author.id)};")
                return
            if player_total > dealer_total:
                embed = discord.Embed(title="Blackjack", description=f"You won `${addcomma(self.bet)}`!", color=discord.Color.green())
                embed.add_field(name="You", value=f"`{self.player_cards[0]}` `{self.player_cards[1]}`\nTotal: {player_total}", inline=True)
                embed.add_field(name="Dealer", value=f"`{self.dealer_cards[0]}` `{self.dealer_cards[1]}` `{self.dealer_cards[2]}`\nTotal: {dealer_total}", inline=True)
                await interaction.response.edit_message(embed=embed, view=self)
                cursor.execute(f"UPDATE users SET coins = coins + {addcomma(self.bet)} WHERE id = {str(self.ctx.author.id)};")
                return
            if dealer_total > 21:
                embed = discord.Embed(title="Blackjack", description=f"You won `${addcomma(self.bet)}`!", color=discord.Color.green())
                embed.add_field(name="You", value=f"`{self.player_cards[0]}` `{self.player_cards[1]}`\nTotal: {player_total}", inline=True)
                embed.add_field(name="Dealer", value=f"`{self.dealer_cards[0]}` `{self.dealer_cards[1]}` `{self.dealer_cards[2]}`\nTotal: {dealer_total}", inline=True)
                await interaction.response.edit_message(embed=embed, view=self)
                cursor.execute(f"UPDATE users SET coins = coins + {addcomma(self.bet)} WHERE id = {str(self.ctx.author.id)};")
                return
            if player_total < dealer_total:
                embed = discord.Embed(title="Blackjack", description=f"You lost :(\nYou lost `${addcomma(self.bet)}`", color=discord.Color.red())
                embed.add_field(name="You", value=f"`{self.player_cards[0]}` `{self.player_cards[1]}`\nTotal: {player_total}", inline=True)
                embed.add_field(name="Dealer", value=f"`{self.dealer_cards[0]}` `{self.dealer_cards[1]}` `{self.dealer_cards[2]}`\nTotal: {dealer_total}", inline=True)
                await interaction.response.edit_message(embed=embed, view=self)
                cursor.execute(f"UPDATE users SET coins = coins - {addcomma(self.bet)} WHERE id = {str(self.ctx.author.id)};")
                return
            if player_total == dealer_total:
                embed = discord.Embed(title="Blackjack", description="Tie!\nYou didn't loose any money", color=discord.Color.gold())
                embed.add_field(name="You", value=f"`{self.player_cards[0]}` `{self.player_cards[1]}`\nTotal: {player_total}", inline=True)
                embed.add_field(name="Dealer", value=f"`{self.dealer_cards[0]}` `{self.dealer_cards[1]}` `{self.dealer_cards[2]}`\nTotal: {dealer_total}", inline=True)
                await interaction.response.edit_message(embed=embed, view=self)
                return
            
    @discord.ui.button(label="Quit", style=discord.ButtonStyle.red)
    async def quit_callback(self, button, interaction):
        if interaction.user.id == self.ctx.author.id:
            self.clear_items()
            embed = discord.Embed(title="Blackjack", description="You quit the game", color=discord.Color.red())
            await interaction.response.edit_message(embed=embed, view=self)
            return
        else: 
            await interaction.response.send_message(f"{interaction.user.name}, you cannot quit someone else's game.", ephemeral=True)
            return
        
    async def on_timeout(self): return

class Economy(commands.Cog):    
    def __init__(self, bot): 
        self.bot = bot
        self.daily_pay = const.load.daily_pay
        self.weekly_pay = const.load.weekly_pay
        self.monthly_pay = const.load.monthly_pay
        
    #Commands to add: $shop, $inventory, $use, $stats
        
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
        embed = discord.Embed(title=f"You were given `${amount}` coins for begging.")
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
        await ctx.send(embed=discord.Embed(title=f"You deposited `${addcomma(amount)}` coins."))
        
    @commands.command(name="withdraw", brief="Withdraw coins", aliases=["with"])
    async def withdraw(self, ctx, amount: str = 0):
        if connect.is_connected(): pass
        else: connect.reconnect(attempts=3)
        try:
            if int(amount) == 0:
                await ctx.send(embed=discord.Embed(title="Please specify an amount of coins to withdraw.", color=discord.Color.red()))
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
        await ctx.send(embed=discord.Embed(title=f"You withdrew `${addcomma(amount)}` coins."))
        
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
            embed = discord.Embed(title="Balance", description=f"**Wallet:** `${addcomma(coins)}`\n**Bank:** `${addcomma(bank)}`",)
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
            embed = discord.Embed(title=f"{user.name}#{user.discriminator}'s balance", description=f"**Wallet:** `${addcomma(coins)}`\n**Bank:** `${addcomma(bank)}`")
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
            await ctx.send(embed=discord.Embed(title="You don't have any coins to pay. Try withdrawing some coins", color=discord.Color.red()))
            return
        
        cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
        if cursor.fetchone()[0] < amount:
            await ctx.send(embed=discord.Embed(title=f"You don't have enough coins to pay `${addcomma(amount - tax)}` (+ `{tax}` tax)", color=discord.Color.red()))
            return
        
        cursor.execute(f"SELECT * FROM users WHERE id = {str(user.id)};")
        if cursor.fetchone() is None:
            cursor.execute(f"INSERT INTO users (id, coins, bank) VALUES ({str(user.id)}, {str(0)}, {str(0)});")
        
        
        cursor.execute(f"UPDATE users SET coins = coins - {str(amount)} WHERE id = {str(ctx.author.id)}")
        cursor.execute(f"UPDATE users SET coins = coins + {str(amount - tax)} WHERE id = {str(user.id)}")
        connect.commit()
        embed=discord.Embed(title=f"You paid {user.name}")
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
            await ctx.send(embed=discord.Embed(title=f"You worked hard, you got full pay: `${addcomma(pay)}`"))
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
        else:
            await ctx.send(embed=discord.Embed(title=f"your boss forgot to pay you", color=discord.Color.red()))
            
    @commands.command(name="daily", brief="Get your daily coins")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        if connect.is_connected(): pass
        else: connect.reconnect(attempts=3)
        
        cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
        if cursor.fetchone() is None:
            cursor.execute(f"INSERT INTO users (id, coins, bank) VALUES ({str(ctx.author.id)}, {str(0)}, {str(0)});")
            
        cursor.execute(f"UPDATE users SET coins = coins + {str(self.daily_pay)} WHERE id = {str(ctx.author.id)}")
        connect.commit()
        embed=discord.Embed(title=f"{ctx.author.name}'s coins", description=f"`${addcomma(self.daily_pay)}` was added to your wallet!\n\nYour next daily is in **1 day**")
        await ctx.send(embed=embed)
        
    @commands.command(name="weekly", brief="Get your weekly coins")
    @commands.cooldown(1, 604800, commands.BucketType.user)
    async def weekly(self, ctx):
        if connect.is_connected(): pass
        else: connect.reconnect(attempts=3)
        
        cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
        if cursor.fetchone() is None:
            cursor.execute(f"INSERT INTO users (id, coins, bank) VALUES ({str(ctx.author.id)}, {str(0)}, {str(0)});")
            
        cursor.execute(f"UPDATE users SET coins = coins + {str(self.weekly_pay)} WHERE id = {str(ctx.author.id)}")
        connect.commit()
        embed=discord.Embed(title=f"{ctx.author.name}'s coins", description=f"`${addcomma(self.weekly_pay)}` was added to your wallet!\n\nYour next weekly is in **1 week**")
        await ctx.send(embed=embed)
        
    @commands.command(name="monthly", brief="Get your monthly coins")
    @commands.cooldown(1, 2678400, commands.BucketType.user)
    async def monthly(self, ctx):
        if connect.is_connected(): pass
        else: connect.reconnect(attempts=3)
        
        cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
        if cursor.fetchone() is None:
            cursor.execute(f"INSERT INTO users (id, coins, bank) VALUES ({str(ctx.author.id)}, {str(0)}, {str(0)});")
            
        cursor.execute(f"UPDATE users SET coins = coins + {str(self.monthly_pay)} WHERE id = {str(ctx.author.id)}")
        connect.commit()
        embed=discord.Embed(title=f"{ctx.author.name}'s coins", description=f"`${addcomma(self.monthly_pay)}` was added to your wallet!\n\nYour next monthly is in **1 month**")
        await ctx.send(embed=embed)
        
        
    @commands.command(name="rob", brief="Rob a user", aliases=["steal"])
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def rob(self, ctx, user: discord.Member):
        if connect.is_connected(): pass
        else: connect.reconnect(attempts=3)
        
        cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
        if cursor.fetchone() is None:
            cursor.execute(f"INSERT INTO users (id, coins, bank) VALUES ({str(ctx.author.id)}, {str(0)}, {str(0)});")
            
        cursor.execute(f"SELECT * FROM users WHERE id = {str(user.id)};")
        if cursor.fetchone() is None:
            embed = discord.Embed(title="This user has no money in their wallet or bank. Not worth it bro", color=discord.Color.red())
            await ctx.send(embed=embed)
            
        cursor.execute(f"SELECT * FROM users WHERE id = {str(user.id)};")
        coins = cursor.fetchone()[0]
        
        if coins == 0:
            await ctx.send(embed=discord.Embed(title="This user has no money in their wallet. Not worth it bro", color=discord.Color.red()))
            return
            
        amt = random.randint(1, coins)
        
        chance_of_robbing = random.randint(1, 100)
        if chance_of_robbing <= 50:
            await ctx.send(embed=discord.Embed(title="You got caught stealing from this user", color=discord.Color.red()))
            cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
            coins = cursor.fetchone()[0]
            if coins > 0:   
                cursor.execute(f"UPDATE users SET coins = coins - {str(coins / 2)} WHERE id = {str(ctx.author.id)}") # 50% of your coins are taken
                return
            else:
                cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
                bank = cursor.fetchone()[2]
                if bank > 0:
                    cursor.execute(f"UPDATE users SET bank = bank - {str(bank / 2)} WHERE id = {str(ctx.author.id)}")
                    return
                else:
                    cursor.execute(f"UPDATE users SET bank = -100000 WHERE id = {str(ctx.author.id)}")
        
        cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
        coins = cursor.fetchone()[0]
        cursor.execute(f"UPDATE users SET coins = coins + {str(amt)} WHERE id = {str(ctx.author.id)}")
        
        cursor.execute(f"SELECT * FROM users WHERE id = {str(user.id)};")
        coins = cursor.fetchone()[0]
        cursor.execute(f"UPDATE users SET coins = coins - {str(amt)} WHERE id = {str(user.id)}")
        
        tiny_amt = coins / 4
        medium_amt = coins / 2
        big_amt = coins / .5
        
        if amt <= tiny_amt: 
            embed = discord.Embed(title=f"You stole a tiny amount (`${addcomma(amt)}`) from {user.name}")
            await ctx.send(embed=embed)
            return
        elif amt <= medium_amt: 
            embed = discord.Embed(title=f"You stole a decent amount (`${addcomma(amt)})` from {user.name}")
            await ctx.send(embed=embed)
            return
        elif amt <= big_amt:
            embed = discord.Embed(title=f"You stole a load! (`${addcomma(amt)}`) from {user.name}")
            await ctx.send(embed=embed)
            return
        
    @commands.command(name="economy", brief="See the top X users")
    async def economy(self, ctx, amount: int = 10, type: str = "bank"):
        if connect.is_connected(): pass
        else: connect.reconnect(attempts=3)
        
        if amount == 0: amount = 10
        
        if type == "coins":
            cursor.execute(f"SELECT * FROM users ORDER BY coins DESC LIMIT {str(amount)};")
            users = cursor.fetchall()
            embed = discord.Embed(title="Top users")
            for i in range(len(users)):
                user = self.bot.get_user(users[i][1])
                embed.add_field(name=f"{i + 1}. {user.name}", value=f"Coins: `${addcomma(users[i][0])}`", inline=False)
            await ctx.send(embed=embed)
            connect.commit()
            return
        elif type == "bank":
            cursor.execute(f"SELECT * FROM users ORDER BY bank DESC LIMIT {str(amount)};")
            users = cursor.fetchall()
            embed = discord.Embed(title="Top users")
            for i in range(len(users)):
                user = self.bot.get_user(users[i][1])
                embed.add_field(name=f"{i + 1}. {user.name}", value=f"Bank: `${addcomma(users[i][2])}`", inline=False)
            await ctx.send(embed=embed)
            connect.commit()
            return
        else:
            await ctx.send(embed=discord.Embed(title="Invalid type, types are **coins** or **bank**", color=discord.Color.red()))
            return
    
    @commands.command(name="stock", brief="See the stock market", aliases=["stocks"])
    async def stock(self, ctx):
        if connect.is_connected(): pass
        else: connect.reconnect(attempts=3)
        
        cursor.execute(f"SELECT * FROM stocks ORDER BY price DESC ")
        stocks = cursor.fetchall()
        embed = discord.Embed(title="Stock market")
        for i in range(len(stocks)):
            embed.add_field(name=f"{i + 1}. {stocks[i][1]}", value=f"Price: `${addcomma(stocks[i][0])}` `{stocks[i][2]}`", inline=False)
            
        await ctx.send(embed=embed)
        connect.commit()
        return
        
    @commands.command(name="invest", brief="Invest in the stock market", aliases=["buy"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def invest(self, ctx, stock: str, shares: int):
        if connect.is_connected(): pass
        else: connect.reconnect(attempts=3)
        
        stock = stock.upper()
                
        cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
        if cursor.fetchone() is None:
            embed = discord.Embed(title="You can't invest if you don't have a bank.", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        
        cursor.execute(f"SELECT * FROM stocks WHERE name = '{stock}'")
        if cursor.fetchone() is None:
            embed = discord.Embed(title="That stock doesn't exist.", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        
        cursor.execute(f"SELECT * FROM stocks WHERE name = '{stock}'")
        stock_price = cursor.fetchone()[0]
        
        cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
        bank = cursor.fetchone()[2]
        
        how_much_to_pay = (shares * stock_price)
        tax = round(how_much_to_pay / 100) 
        how_much_to_pay = (how_much_to_pay + tax) 
        
        if bank < how_much_to_pay:
            embed = discord.Embed(title=f"You don't have enough money to invest `{str(shares)}` shares in this stock. (+ `{tax}` tax)", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        
        cursor.execute(f"UPDATE users SET bank = bank - {str(how_much_to_pay)} WHERE id = {str(ctx.author.id)}")
        
        cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
        shares_owned = cursor.fetchone()[3]
        
        shares_owned = shares_owned.split("|")
        
        AAPL = shares_owned[0]
        GOOGL = shares_owned[1]
        AMZN = shares_owned[2]
        NVA = shares_owned[3]
        
        if stock == "AAPL":
            shares_owned[0] = int(int(AAPL) + shares)
            cursor.execute(f"UPDATE users SET shares = '{shares_owned[0]}|{shares_owned[1]}|{shares_owned[2]}|{shares_owned[3]}' WHERE id = {str(ctx.author.id)}")
        elif stock == "GOOGL":
            shares_owned[1] = int(int(GOOGL) + shares)
            cursor.execute(f"UPDATE users SET shares = '{shares_owned[0]}|{shares_owned[1]}|{shares_owned[2]}|{shares_owned[3]}' WHERE id = {str(ctx.author.id)}")
        elif stock == "AMZN":
            shares_owned[2] = int(int(AMZN) + shares)
            cursor.execute(f"UPDATE users SET shares = '{shares_owned[0]}|{shares_owned[1]}|{shares_owned[2]}|{shares_owned[3]}' WHERE id = {str(ctx.author.id)}")
        elif stock == "NVA":
            shares_owned[3] = int(int(NVA) + shares)
            cursor.execute(f"UPDATE users SET shares = '{shares_owned[0]}|{shares_owned[1]}|{shares_owned[2]}|{shares_owned[3]}' WHERE id = {str(ctx.author.id)}")
        
        a = int(stock_price) / 1024
        b = random.randint(1, int(a))
        cursor.execute(f"UPDATE stocks SET price = price + {str(b)} WHERE name = '{stock}'")
                    
        connect.commit()
        embed = discord.Embed(title=f"Investment")
        embed.add_field(name="Stock", value=f"{stock}", inline=False)
        embed.add_field(name="Shares", value=f"`{shares}`", inline=False)
        embed.add_field(name="Share price", value=f"`${addcomma(stock_price)}`", inline=False)
        embed.add_field(name="Tax", value=f"`${addcomma(tax)}`", inline=False)
        embed.add_field(name="Total", value=f"`${addcomma(how_much_to_pay)}`", inline=False)
        await ctx.send(embed=embed)
        return
    
    @commands.command(name="sell", brief="Sell a stock")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def sell(self, ctx, stock: str, shares: str = "1"):
        if connect.is_connected(): pass
        else: connect.reconnect(attempts=3)
        
        stock = stock.upper()
        
        cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
        if cursor.fetchone() is None:
            embed = discord.Embed(title="You can't sell if you don't have a bank.", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        
        cursor.execute(f"SELECT * FROM stocks WHERE name = '{stock}'")
        if cursor.fetchone() is None:
            embed = discord.Embed(title="That stock doesn't exist.", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        
        cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
        shares1 = cursor.fetchone()[3]    
        shares1 = shares1.split("|")
        
        AAPL = shares1[0]
        GOOGL = shares1[1]
        AMZN = shares1[2]
        NVA = shares1[3]
        
        try:
            shares = int(shares)
        except:
            if str(shares) == "all":
                if stock == "AAPL": shares = int(AAPL)
                elif stock == "GOOGL": shares = int(GOOGL)
                elif stock == "AMZN": shares = int(AMZN)
                elif stock == "NVA": shares = int(NVA)
            else:
                embed = discord.Embed(title="Invalid number of shares.", color=discord.Color.red())
                await ctx.send(embed=embed)
                return
                    
        
        if stock == "AAPL":
            if int(AAPL) < shares:
                embed = discord.Embed(title="You don't have that many shares.", color=discord.Color.red())
                await ctx.send(embed=embed)
                return
            
        elif stock == "GOOGL":
            if int(GOOGL) < shares:
                embed = discord.Embed(title="You don't have that many shares.", color=discord.Color.red())
                await ctx.send(embed=embed)
                return
            
        elif stock == "AMZN":
            if int(AMZN) < shares:
                embed = discord.Embed(title="You don't have that many shares.", color=discord.Color.red())
                await ctx.send(embed=embed)
                return
        
        elif stock == "NVA":
            if int(NVA) < shares:
                embed = discord.Embed(title="You don't have that many shares.", color=discord.Color.red())
                await ctx.send(embed=embed)
                return
        
        cursor.execute(f"SELECT * FROM stocks WHERE name = '{stock}'")
        price = cursor.fetchone()[0]
        
        tax = round(price / 100) 
        how_much_you_get = (price - tax)
                
        cursor.execute(f"UPDATE users SET bank = bank + {str(how_much_you_get * shares)} WHERE id = {str(ctx.author.id)}") 

        cursor.execute(f"UPDATE stocks SET price = price - {str(shares)} WHERE name = '{stock}'")
        
        if stock == "AAPL": shares1[0] = int(int(AAPL) - shares)
        elif stock == "GOOGL": shares1[1] = int(int(GOOGL) - shares)
        elif stock == "AMZN": shares1[2] = int(int(AMZN) - shares)
        elif stock == "NVA": shares1[3] = int(int(NVA) - shares)
            
        cursor.execute(f"UPDATE users SET shares = '{shares1[0]}|{shares1[1]}|{shares1[2]}|{shares1[3]}' WHERE id = {str(ctx.author.id)}")
        
        embed = discord.Embed(title=f"Sold successfully")
        embed.add_field(name="Stock", value=f"{stock}", inline=False)
        embed.add_field(name="Shares", value=f"`{shares}`", inline=False)
        embed.add_field(name="Share price", value=f"`${addcomma(price)}`", inline=False)
        embed.add_field(name="Tax", value=f"`-${addcomma(tax)} per share`", inline=False)
        embed.add_field(name="Total earned", value=f"`${addcomma(how_much_you_get * shares)}`", inline=False)
        await ctx.send(embed=embed)
        connect.commit()
        return
    
    @commands.command(name="shares", brief="See how many shares you have")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def shares(self, ctx):
        if connect.is_connected(): pass
        else: connect.reconnect(attempts=3)
        
        cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
        if cursor.fetchone() is None:
            embed = discord.Embed(title="You have no shares", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        
        cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
        shares1 = cursor.fetchone()[3]
        shares1 = shares1.split("|")
        
        AAPL = shares1[0]
        GOOGL = shares1[1]
        AMZN = shares1[2]
        NVA = shares1[3]
        
        embed = discord.Embed(title="Your shares")
        embed.add_field(name="Apple", value=f"`{str(AAPL)}`", inline=False)
        embed.add_field(name="Google", value=f"`{str(GOOGL)}`", inline=False)
        embed.add_field(name="Amazon", value=f"`{str(AMZN)}`", inline=False)
        embed.add_field(name="Nvidia", value=f"`{str(NVA)}`", inline=False)
        embed.set_footer(text=f"{ctx.author.name}'s shares", icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
        connect.commit()
        return
    
    @commands.command(name="blackjack", brief="Play blackjack", aliases=["bj"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def blackjack(self, ctx, bet):
        if connect.is_connected(): pass
        else: connect.reconnect(attempts=3)
        
        cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
        if cursor.fetchone() is None:
            embed = discord.Embed(title="You have to have a wallet to bet", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        
        cursor.execute(f"SELECT * FROM users WHERE id = {str(ctx.author.id)};")
        wallet = cursor.fetchone()[0]
        if int(wallet) < int(bet):
            embed = discord.Embed(title="You don't have that much money lol", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        
        if int(bet) < 1500: 
            embed = discord.Embed(title="You need to bet at least `$1,500`", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        
        player_cards = []
        dealer_cards = []
        
        player_cards.append(random.choice(cards))
        player_cards.append(random.choice(cards))
        dealer_cards.append(random.choice(cards))
        embed = discord.Embed(title="Blackjack")
        embed.add_field(name="Dealer", value=f"`{dealer_cards[0]}` `?`", inline=True)
        embed.add_field(name="You", value=f"`{player_cards[0]}` `{player_cards[1]}`", inline=True)
        embed.set_footer(text=f"{ctx.author.name}'s blackjack game", icon_url=ctx.author.avatar)
            
        view = viewstuff(ctx, player_cards, dealer_cards, bet, wallet)
        await ctx.send(embed=embed, view=view)
        
    
    
def setup(bot): bot.add_cog(Economy(bot))