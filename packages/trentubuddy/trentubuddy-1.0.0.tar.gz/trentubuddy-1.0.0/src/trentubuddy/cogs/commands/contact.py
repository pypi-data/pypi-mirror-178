#Commands for contact and children

import discord
from discord.ext import commands


class Contact(commands.Cog):

    
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="contact", invoke_without_command=True, case_insensitive=True, pass_context=True)
    async def contact(self, ctx):
        await ctx.send("**COIS Faculty Members\nList Updated: November 08/22\n\
**To access information, please type prefix '!' followed by contact and the LAST name of the\
 faculty member you wish to reach\n`Available Options:`\n\
Richard HURLEY\nWenying FENG\nBrian PATRICK\nSabine McCONNELL\nOmar ALAM\n\
Fadi ALZHOURI\nBrian SRIVASTAVA\nSofie ANDREOU\nJacques BELAND\nBrian HIRCOCK\n\
Jamie MITCHELL\nPeter NORTHROP\nStephen REGOCZEI\nNancy SMITH\nGraeme YOUNG\nElissa ONIELL\nOther")

# creds to patrick haugh on stackoverflow

    @contact.command()
    async def Hurley(self, ctx):
        embed=discord.Embed(title="Richard Hurley", description="Department Chair and Full-Time Professor", color=0x3a8d34)
        embed.add_field(name="Office Location", value="OC 102.3", inline=True)
        embed.add_field(name="Phone Number", value="(705) 748 1011 ext. 7542", inline=True)
        embed.add_field(name="Email", value="rhurley@trentu.ca", inline=False)
        await ctx.send(embed=embed)

    @contact.command()
    async def Feng(self, ctx):
        embed=discord.Embed(title="Wenying Feng", description="Professor", color=0x3a8d34)
        embed.add_field(name="Office Location", value="OC 102.9", inline=True)
        embed.add_field(name="Phone Number", value="(705) 748 1011 ext. 7249", inline=True)
        embed.add_field(name="Email", value="wfeng@trentu.ca", inline=False)
        await ctx.send(embed=embed)

    @contact.command()
    async def Patrick(self, ctx):
        embed=discord.Embed(title="Brian Patrick", description="Associate Professor", color=0x3a8d34)
        embed.add_field(name="Office Location", value="OC 102.8", inline=True)
        embed.add_field(name="Phone Number", value="(705) 748 1011 ext. 7804", inline=True)
        embed.add_field(name="Email", value="bpatrick@trentu.ca", inline=False)
        await ctx.send(embed=embed)

    @contact.command()
    async def McConnell(self, ctx):
        embed=discord.Embed(title="Sabine McConnell", description="Associate Professor", color=0x3a8d34)
        embed.add_field(name="Office Location", value="OC 102.7", inline=True)
        embed.add_field(name="Phone Number", value="(705) 748 1011 ext. 7803", inline=True)
        embed.add_field(name="Email", value="sabinemcconnell@trentu.ca", inline=False)
        await ctx.send(embed=embed)

    @contact.command()
    async def Alam(self, ctx):
        embed=discord.Embed(title="Omar Alam", description="Assistant Professor", color=0x3a8d34)
        embed.add_field(name="Phone Number", value="(705) 748 1011 ext. 7347", inline=True)
        embed.add_field(name="Email", value="omaralam@trentu.ca", inline=False)
        await ctx.send(embed=embed)

    @contact.command()
    async def Alzhouri(self, ctx):
        embed=discord.Embed(title="Fadi Alzhouri", description="Assistant Professor", color=0x3a8d34)
        embed.add_field(name="Phone Number", value="(705) 748 1011 ext. 7750", inline=True)
        embed.add_field(name="Email", value="fadialzhouri@trentu.ca", inline=False)
        await ctx.send(embed=embed)

    @contact.command()
    async def Sri(self, ctx):
        embed=discord.Embed(title="Brian Srivastava", description="Lecturer", color=0x3a8d34)
        embed.add_field(name="Office Location", value="OC 102.6", inline=True)
        embed.add_field(name="Phone Number", value="(705) 748 1011", inline=True)
        embed.add_field(name="Email", value="bsrivastava@trentu.ca", inline=False)
        await ctx.send(embed=embed)

    @contact.command()
    async def Andreou(self, ctx):
        embed=discord.Embed(title="Sofie Andreou", color=0x3a8d34)
        embed.add_field(name="Email", value="sofieandreou@trentu.ca", inline=False)
        await ctx.send(embed=embed)

    @contact.command()
    async def Beland(self, ctx):
        embed=discord.Embed(title="Jacques Beland", color=0x3a8d34)
        embed.add_field(name="Email", value="jacquesbeland@trentu.ca", inline=False)
        await ctx.send(embed=embed)

    @contact.command()
    async def Hircock(self, ctx):
        embed=discord.Embed(title="Brian Hircock", color=0x3a8d34)
        embed.add_field(name="Email", value="bhircock@trentu.ca", inline=False)
        await ctx.send(embed=embed)

    @contact.command()
    async def Mitchell(self, ctx):
        embed=discord.Embed(title="Jamie Mitchell", color=0x3a8d34)
        embed.add_field(name="Email", value="jamiemitchell@trentu.ca", inline=False)
        await ctx.send(embed=embed)

    @contact.command()
    async def Northrop(self, ctx):
        embed=discord.Embed(title="Peter Northrop", color=0x3a8d34)
        embed.add_field(name="Email", value="pnorthrop@trentu.ca", inline=False)
        await ctx.send(embed=embed)

    @contact.command()
    async def Regoczei(self, ctx):
        embed=discord.Embed(title="Stephen Regoczei", color=0x3a8d34)
        embed.add_field(name="Email", value="sregoczei@trentu.ca", inline=False)
        await ctx.send(embed=embed)

    @contact.command()
    async def Smith(self, ctx):
        embed=discord.Embed(title="Nancy Smith", color=0x3a8d34)
        embed.add_field(name="Email", value="nmsmith@trentu.ca", inline=False)
        await ctx.send(embed=embed)

    @contact.command()
    async def Young(self, ctx):
        embed=discord.Embed(title="Graeme Young", color=0x3a8d34)
        embed.add_field(name="Email", value="gyoung@trentu.ca", inline=False)
        await ctx.send(embed=embed)

    @contact.command()
    async def ONeill(self, ctx):
        embed=discord.Embed(title="Elissa O'Neill", description="Academic Administrative Assistant", color=0x3a8d34)
        embed.add_field(name="Office Location", value="OC 102.6", inline=True)
        embed.add_field(name="Phone Number", value="(705) 748 1011 ext. 7802", inline=True)
        embed.add_field(name="Email", value="cois@trentu.ca", inline=False)
        await ctx.send(embed=embed)

    @contact.command()
    async def Other(self, ctx):
        embed=discord.Embed(title="Other Contacts", color=0x3a8d34)
        embed.add_field(name="COIS General Inquiries Email", value="cois@trentu.ca", inline=False)
        embed.add_field(name="COIS Jobs", value="coisjobs@trentu.ca", inline=False)
        await ctx.send(embed=embed)


#Required to add the functions
async def setup(bot):
    await bot.add_cog(Contact(bot))