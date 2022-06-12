import random, discord, re, lib.color as c
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @commands.command(aliases=['8ball'], brief="Ask a question and I'll answer it")
    async def _8ball(self, ctx, *, question):
        responses = [
        discord.Embed(title='🎱 It is certain.', footer=question),
        discord.Embed(title='🎱 It is decidedly so.', footer=question),
        discord.Embed(title='🎱 Without a doubt.', footer=question),
        discord.Embed(title='🎱 Yes - definitely.', footer=question),
        discord.Embed(title='🎱 You may rely on it.', footer=question),
        discord.Embed(title='🎱 Most likely.', footer=question),
        discord.Embed(title='🎱 Outlook good.', footer=question),
        discord.Embed(title='🎱 Yes.', footer=question),
        discord.Embed(title='🎱 Signs point to yes.', footer=question),
        discord.Embed(title='🎱 Reply hazy, try again.', footer=question),
        discord.Embed(title='🎱 Ask again later.', footer=question),
        discord.Embed(title='🎱 Better not tell you now.', footer=question),
        discord.Embed(title='🎱 Cannot predict now.', footer=question),
        discord.Embed(title='🎱 Concentrate and ask again.', footer=question),
        discord.Embed(title="🎱 Don't count on it."),
        discord.Embed(title='🎱 My reply is no.', footer=question),
        discord.Embed(title='🎱 My sources say no.', footer=question),
        discord.Embed(title='🎱 Outlook not very good.', footer=question),
        discord.Embed(title='🎱 Very doubtful.', footer=question)]
        responses = random.choice(responses)
        await ctx.send(embed=responses)

    @commands.command(aliases=['pick'], brief="A random choice from a list of choices")
    async def choose(self, ctx):
        choices = ["Earth", "Water", "Fire", "Air", "Wind"]
        await ctx.send(embed=discord.Embed(f'I choose: {random.choice(choices)}'))

    @commands.command(brief="Roll a dice")
    async def dice(self, ctx, *, msg="1"):
        dice_rolls = []
        dice_roll_ints = []
        try:
            dice, sides = re.split("[d\s]", msg)
        except ValueError:
            dice = msg
            sides = "6"
        try:
            for roll in range(int(dice)):
                result = random.randint(1, int(sides))
                dice_rolls.append(str(result))
                dice_roll_ints.append(result)
        except ValueError:
            return await ctx.send(embed=discord.Embed(title="Error", description="Invalid syntax", color=0xFF0000))
        embed = discord.Embed(title="Dice rolls:", description=' '.join(dice_rolls))
        embed.add_field(name="Total:", value=sum(dice_roll_ints))
        await ctx.send("", embed=embed)
        
    @commands.command(pass_context=True, aliases=['eb'], brief="Build a custom embed")
    async def embedBuilder(self, ctx, splitcharacter, titleUrl, color, *, msg):
        #Syntax example: $eb | yes 8E72BE https://google.com|Get help|Click the blue text, and Google your problem.
        # explain: cmd, character to split (e/e/e, e|e|e), titleUrl yes or no, color code, (if titleUrl is yes, link)<separator>title<separator>description  
        
        
        if titleUrl == "yes":
            if msg.startswith("http"):
                msg = msg.split(str(splitcharacter))
                embed = discord.Embed(title=msg[1], url=msg[0], description=msg[2], color=int(color, 16))
            else: return await ctx.send(embed=discord.Embed(title="Error", description="Invalid syntax: [Not a real URL]", color=0xFF0000))
        elif titleUrl == "no":
            msg = msg.split(str(splitcharacter))
            embed = discord.Embed(title=msg[0], description=msg[1], color=int(color, 16))
        
        await ctx.send(embed=embed)
def setup(bot): bot.add_cog(Fun(bot))
print(c.color.GREEN + "Fun cog loaded" + c.color.END)