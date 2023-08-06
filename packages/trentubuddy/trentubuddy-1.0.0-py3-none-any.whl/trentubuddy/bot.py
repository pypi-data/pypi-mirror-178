# bot.py
# Author(s):    Zachary Bricknell
#
# Routine:      TrentUBuddy
# 
# Desc: This bot is created to utilize the discord.py plugin to assist students in
#   inding general information. This is achieved by using web scrapers to compile data
#   and display a formatted output of the results. This is packaged into PYPI to provide
#   easy installation by only requiring a discord token to execute. The discord token
#   is saved in plain text, use appropriate security if needed. 
#
# changelog:    11/10/2022 First iteration complete fully executable locally
#               11/21/2022 Prepared for PYPI changed all pathing and implemented file creation
#               11/27/2022 implemented better error handling on inital creation and execution

from .scripts import helpers as helper
import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
import sys
import getpass

#Get proper  pathing
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
env_file_path = file_dir + "/env/.env"
#changes \\ to / if linux system *Windows will read / regardless but keeping code here for now*
cog_path = os.path.dirname(os.path.realpath(__file__)) + helper.os_path_helper("\\cogs")

#Bot options
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(intents = discord.Intents.all(), command_prefix = '!', help_command=None, case_insensitive=True)

#recursively get every extension for every .py file in the path or subdirectories as well as 
#use the apporpriate structure for cogs with a "." to join the path
async def load_extensions(extensions_path, folder_path = "" ): 
    try:   
        if(folder_path == ""):
            #folder path must start at the given rirectory is located so we take the last entry of the input
            folder_path = extensions_path.rsplit(helper.os_path_helper("\\"), 1)[-1]    
        for filename in os.listdir(extensions_path):
            if(os.path.isdir(os.path.join(extensions_path, filename))):
                #recursively load in the new path with a delimiter of "." to be used in load_extension
                await load_extensions(extensions_path + helper.os_path_helper("\\") + filename, folder_path + "." + filename)
            if filename.endswith('.py'):    
                #remove .py for each filename         
                await bot.load_extension(f'{folder_path}.{filename[:-3]}')    
    except:
        return -1    

#This is the new way to do bot.run(TOKEN) by loading the cogs first.
def main():
    asyncio.run(load_bot())
    
#To be called from main.py to execute this script.
async def load_bot():
    async with bot:
        token_reset_flag = 1        
        json_files = ["specialties.json", "ac_link.json"]
        try:
            if not os.path.exists("data"):
                os.makedirs("data")

            for new_file in json_files:
                with open("data/" + new_file, "w+"): pass

            if (await load_extensions(cog_path)) == -1:
                print("Error loading cogs...")
                return -1

            if os.path.exists(env_file_path):
                user_input = input("Would you like to use the existing token?...(Y/n)")
                if (user_input.lower() == "y"):                    
                    token_reset_flag = 0

            if token_reset_flag == 1:
                with open(env_file_path, "w+") as env_file:                    
                    new_discord_token = getpass.getpass("Please enter new Token: ")
                    env_file.write("DISCORD_TOKEN=" + new_discord_token)
                    env_file.close()

            load_dotenv(env_file_path)
            TOKEN = os.getenv('DISCORD_TOKEN')
            await bot.start(TOKEN)

        except discord.errors.LoginFailure:
            print("Token was invalid, Please restart and enter a valid token...")
            return -1

        except:
            print("Error with bot startup", sys.exc_info()[0])
            return -1

if __name__ == "__main__":
    asyncio.run(main())