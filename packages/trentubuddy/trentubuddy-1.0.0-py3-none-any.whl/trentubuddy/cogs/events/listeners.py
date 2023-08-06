import discord
from discord.ext import commands


class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'TrentU Buddy... ONLINE !!!')


    #When someone joins the server they get a direct message  
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, I am your student helper bot \nStarter Commands Here')

    #allowing for the bot to read events from messages and guilds(servers)
    #do not disbale these for now
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if guild.system_channel:
            await guild.system_channel.send("Test")

#Required to add the functions
async def setup(bot):
    await bot.add_cog(Listeners(bot))