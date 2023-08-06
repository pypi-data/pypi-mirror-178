#Commands for contact and children

import os
import sys
import discord
from discord.ext import commands
import json
from scripts import helpers as helper
from scripts import cs_specialty_scraper as cs_specialties
from scripts import ac_link_scraiper as academic_calendar
import time
from pathlib import Path
import psutil
import time
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
path_to_data = os.getcwd()

specialties_path = os.getcwd() + "/data/specialties.json"
ac_path = os.getcwd() + "/data/ac_link.json"


class Specialties(commands.Cog):

    def __init__(self, bot):
        self.bot = bot   

    @commands.command(case_insensitive=True, aliases=["sp"])
    async def specialties(self, ctx):          
        file_age = helper.SinceLastModified(specialties_path)  
        print(file_age) 
        if((file_age > 10) | (file_age <0)):
            await ctx.send("Let me get that information for you...")
            if cs_specialties.update_specialties() != 0:
                await ctx.send("Error fetching information...")
                return
        file = open(specialties_path, "r")  
        content = json.load(file)
        file.close()
        for specialty_key, specialty_value in content.items():
            embed=discord.Embed(title=specialty_key, color=0x3a8d34)            
            embed.add_field(name="Requirements:", value="\n\n".join(specialty_value), inline=False)
            await ctx.send(embed=embed)     

    @commands.command(case_insensitive=True, aliases=["academiccalendar", "academic_calendar", "a_c"])
    async def ac(self, ctx):
        delete_timer = 30.0         
        file_age = helper.SinceLastModified(ac_path)   
        if((file_age > 10) | (file_age <0)):
            await ctx.send("Let me get that information for you...", delete_after=delete_timer)
            if academic_calendar.get_ac_link() != 0:
                await ctx.send("Error fetching information...", delete_after=delete_timer)
                return
        file = open(ac_path, "r")         
        content = json.load(file)
        file.close()
        for specialty_key, specialty_value in content.items():
            embed=discord.Embed(title=specialty_key, color=0x3a8d34, url=specialty_value)            
            await ctx.send(embed=embed, delete_after=delete_timer) 
            #only one item should be in the file
            return   

async def setup(bot):
    await bot.add_cog(Specialties(bot))