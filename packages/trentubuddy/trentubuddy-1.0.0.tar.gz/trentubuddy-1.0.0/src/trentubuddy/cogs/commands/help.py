#Commands for contact and children

import discord
from discord.ext import commands
import json
import scripts.helpers as helper

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot   
    
    #help command // what are all the available functions?

    @commands.group(name="help", invoke_without_command=True, case_insensitive=True)
    async def help(self, ctx):
        await ctx.send("Here are the available commands:\n`Hello`: Say hello to the bot \
            \n`Goodbye`: Say goodbye to the bot\n`Contact`: Contact information for COIS faculty members\n`Resources`: Links to different\
            Trent resources\n")

    #this is an example of different sub categories that can be in the
    #overall bot group. Will use this function for specific faculty members.
    @help.command()
    async def booking(self, ctx):
        await ctx.send("Here are the available commands:\n`advising`: Book with Trent's Academic Advising\n\
            `skills`: Book with Academic Skills\n`healthinmotion`: Book with Trent Health in Motion\n\
            `room`: Book a room at Trent's Peterborough campus\n`travel`: Book with Trent International\n\
            `career`: Book with Careerspace\n`peers`: Book with Peer Support\n`coop`: Book with Co-Op")  

#Required to add the functions
async def setup(bot):
    await bot.add_cog(Help(bot))