#Commands for contact and children

import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot   
    
    #help command // what are all the available functions?

    @commands.group(name="help", invoke_without_command=True, case_insensitive=True)
    async def help(self, ctx):
        embed=discord.Embed(title="Command Directory", description="\
        `Contact` Faculty contact list (Use !contact _ for further details)\n\
        `Book` List of booking commands (use !book _ for links)\n\
        `AC` Link to the Academic Callendar using Web Scraper\n\
        `SP` List of CS Specialties and Requirements using Web Scraper", color=0x3a8d34)        
        await ctx.send(embed=embed)        

#Required to add the functions
async def setup(bot):
    await bot.add_cog(Help(bot))