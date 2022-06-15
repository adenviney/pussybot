import discord
from discord.ext import commands

class Server(commands.Cog):
    def __init__(self, bot): self.bot = bot

    # Stats about server
    @commands.group(aliases=['server', 'sinfo', 'si'], brief="Get information about the server", pass_context=True, invoke_without_command=True)
    async def serverinfo(self, ctx, *, msg=""):
        """Shows server info."""
        if ctx.invoked_subcommand is None:
            if msg:
                server = None
                try:
                    float(msg)
                    server = self.bot.get_guild(int(msg))
                    if not server: return await ctx.reply('Server not found.')
                except:
                    for i in self.bot.guilds:
                        if i.name.lower() == msg.lower():
                            server = i
                            break
                    if not server: return
            else: server = ctx.message.guild

            online = 0
            for i in server.members:
                if str(i.status) == 'online' or str(i.status) == 'idle' or str(i.status) == 'dnd':
                    online += 1
            all_users = []
            for user in server.members: all_users.append(f'{user.name}#{user.discriminator}')
            all_users.sort()
            all = '\n'.join(all_users)

            channel_count = len([x for x in server.channels if type(x) == discord.channel.TextChannel])

            role_count = len(server.roles)
            emoji_count = len(server.emojis)

            embed = discord.Embed(title="Server info", color=0x885DD3)
            embed.add_field(name='Name', value=server.name)
            embed.add_field(name='Owner', value=server.owner, inline=False)
            embed.add_field(name='Members', value=server.member_count)
            embed.add_field(name='Currently Online', value=online)
            embed.add_field(name='Text Channels', value=str(channel_count))
            embed.add_field(name='Verification Level', value=str(server.verification_level))
            embed.add_field(name='Number of roles', value=str(role_count))
            embed.add_field(name='Number of emotes', value=str(emoji_count))
            embed.add_field(name='Users', value=ctx.guild.member_count)
            embed.add_field(name='Created At', value=server.created_at.__format__('%A, %d %B %Y %H:%M:%S'))
            embed.set_thumbnail(url=server.icon)
            embed.set_footer(text=f'Server ID: {server.id}')
            await ctx.reply(embed=embed)

    @serverinfo.command(pass_context=True, brief="Get information about the server emojis")
    async def emojis(self, ctx):
        """Displays all emojis on the server."""
        server = ctx.message.guild
        emojis = [str(x) for x in server.emojis]
        embed = discord.Embed(title=f"Emojis in {ctx.guild.name}", color=0x885DD3)
        embed.add_field(name='Emojis:', value="".join(emojis))
        await ctx.message.reply(embed=embed)

    @serverinfo.command(pass_context=True, brief="Get information about a server role")
    async def role(self, ctx, *, msg):
        """Get info about a role."""
        for role in ctx.guild.roles:
            if msg.lower() == role.name.lower() or msg == role.id:
                all_users = [str(x) for x in role.members]
                all_users.sort()
                all_users = ', '.join(all_users)
                em = discord.Embed(title='Role Info', color=role.color)
                em.add_field(name='Name', value=role.name)
                em.add_field(name='ID', value=role.id, inline=False)
                em.add_field(name='Users with this role', value=str(len(role.members)))
                em.add_field(name='Role color hex value', value=str(role.color).upper())
                em.add_field(name='Role color RGB value', value=role.color.to_rgb())
                em.add_field(name='Mentionable', value=role.mentionable)
                if len(role.members) > 10:
                    all_users = all_users.replace(', ', '\n')
                    em.add_field(name='Too many to list', value=all_users, inline=False)
                elif len(role.members) >= 1: em.add_field(name='All users', value=all_users, inline=False)
                else: em.add_field(name='All users', value='There are no users in this role!', inline=False)
                em.add_field(name='Created at', value=role.created_at.__format__('%x at %X'))
                em.set_thumbnail(url=f'http://www.colorhexa.com/{str(role.color).strip("#")}.png')
                return await ctx.reply(content=None, embed=em)
        await ctx.reply(f'Could not find role \'{msg}\'')
        
    @role.error
    async def role_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply('Could not find role.')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('You need to specify a role. (E.g. $serverinfo role <cool person role id>)')

    @commands.command(aliases=['ui', 'uinfo', 'user'], brief="Get information about a user", pass_context=True)
    async def userinfo(self, ctx, user: discord.Member = None):
        """Shows user info."""
        if user is None: user = ctx.author

        permissions = ", ".join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)

        em = discord.Embed(title=f"User info for {user.name}#{user.discriminator}", description=user.mention, color=0x885DD3)
        em.set_thumbnail(url=user.avatar)
        em.add_field(name="Joined at", value=user.joined_at.strftime("%a, %d %b %Y %I:%M %p"))
        em.add_field(name="Registered on", value=user.created_at.strftime("%a, %d %b %Y %I:%M %p"))
        if len(user.roles) > 1:
            roles = " ".join([r.mention for r in user.roles][1:])
            em.add_field(name=f"Roles [{len(user.roles) - 1}]", value=roles, inline=False)
        em.add_field(name="Guild Permissions", value=permissions, inline=False)
        em.add_field(name="Join position", value=str(members.index(user) + 1))
        em.set_footer(text=f"ID: {user.id}")

        await ctx.reply(embed=em)

    @commands.command(aliases=['channel', 'cinfo', 'ci'], brief="Get information about a channel", pass_context=True)
    async def channelinfo(self, ctx, *, channel: discord.TextChannel = None):
        """Shows channel info."""
        if not channel: channel = ctx.channel
        else: channel = self.bot.get_channel(int(channel.id))
        data = discord.Embed(color=0x885DD3)
        if hasattr(channel, 'mention'): data.title = f"Information about {channel.name}"
        if isinstance(channel, discord.TextChannel): _type = "Text"
        elif isinstance(channel, discord.VoiceChannel): _type = "Voice"
        else: _type = "Unknown"
        data.add_field(name="Type", value=_type)
        data.add_field(name="ID", value=channel.id, inline=False)
        if hasattr(channel, 'position'): data.add_field(name="Position", value=channel.position)
        if isinstance(channel, discord.VoiceChannel):
            if channel.user_limit != 0: data.add_field(name="User Number", value=f"{len(channel.voice_members)}/{channel.user_limit}")
            else: data.add_field(name="User Number", value=f"{len(channel.voice_members)}")
            userlist = [r.display_name for r in channel.members]
            if not userlist: userlist = "None"
            else: userlist = "\n".join(userlist)
            data.add_field(name="Users", value=userlist)
            data.add_field(name="Bitrate", value=channel.bitrate)
        elif isinstance(channel, discord.TextChannel):
            try:
                pins = await channel.pins()
                data.add_field(name="Pins", value=len(pins), inline=True)
            except discord.Forbidden:
                pass
            data.add_field(name="Members", value="%s"%len(channel.members))
            if channel.topic: data.add_field(name="Topic", value=channel.topic, inline=False)
            hidden = []
            allowed = []
            for role in channel.changed_roles:
                if role.permissions.read_messages is True:
                    if role.name != "@everyone": allowed.append(role.mention)
                elif role.permissions.read_messages is False:
                    if role.name != "@everyone": hidden.append(role.mention)
            if len(allowed) > 0: data.add_field(name=f'Allowed Roles ({len(allowed)})', value=', '.join(allowed), inline=False)
            if len(hidden) > 0: data.add_field(name=f'Restricted Roles ({len(hidden)})', value=', '.join(hidden), inline=False)
        if channel.created_at: data.set_footer(text=(f"Created on {channel.created_at.strftime('%d %b %Y %H:%M')} ({(ctx.message.created_at - channel.created_at).days} days ago)"))
        await ctx.reply(embed=data)
        
    @channelinfo.error
    async def channelinfo_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply('Could not find that channel.')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f'You need to specify a channel. (E.g. $channelinfo <#{ctx.channel.id}>)')


def setup(bot): bot.add_cog(Server(bot))