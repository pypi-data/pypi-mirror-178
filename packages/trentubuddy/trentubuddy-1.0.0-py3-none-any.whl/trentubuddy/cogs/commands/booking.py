
import discord
from discord.ext import commands

##this file has been completed 16/11/2022


class Booking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #tprent bookings
    ## fix this it looks like shit
    @commands.group(name="book", invoke_without_command=True)
    async def book(self, ctx):
        await ctx.send("**Booking Options**\nHere are the available commands.\n`advising:` Book an appointment with academic advising\n`skills:` Book an appointment with academic skills \
    \n`healthinmotion:` Book an appointment with TrentU Health in Motion at the Athletics Center\
    \n`room:` Book a single pod in Bata Library or a group room\n`travel:` Book an appointment with Trent International\
    \n`career:` Book an appointment with Careerspace\n`peer:` Book an appointment with peer support\
    \n`coop:` Book an appointment with your Co-Op Coordinator")

    @book.command()
    async def advising(self, ctx):
        embed=discord.Embed(title="Academic Advising", color=0x3a8d34, url="https://ccr.trentu.ca/myAccount/aptbooking/aaadvising.htm", \
            description="Click here to book an appointment with Academic Advising")
        await ctx.send(embed=embed)

    @book.command()
    async def skills(self, ctx):
        embed=discord.Embed(title="Academic Skills", color=0x3a8d34, url="https://ccr.trentu.ca/myAccount/aptbooking/asc-appt.htm", \
            description="Click here to book an appointment with Academic Skills")
        await ctx.send(embed=embed)

    @book.command()
    async def healthinmotion(self, ctx):
        embed=discord.Embed(title="Trent Health in Motion", color=0x3a8d34, url="https://trenthealthinmotion.janeapp.com/#/list", \
            description="Click here to book an appointment with Trent Health in Motion")
        embed.set_thumbnail(url="https://trenthealthinmotion.ca/wp-content/uploads/2018/04/slider-1.jpg")
        await ctx.send(embed=embed)

    
    @book.command() #in the future, try to get this so you have the option to choose between single and group rooms to begin with
    async def room(self, ctx):
        embed=discord.Embed(title="Single or Group Room Booking", color=0x3a8d34, url="https://trentu.libcal.com/spaces?lid=2751&gid=0&c=0", \
            description="Click here to book a single study pod or a group room")
        await ctx.send(embed=embed)

    @book.command()
    async def travel(self, ctx):
        embed=discord.Embed(title="Trent International", color=0x3a8d34, url="https://ccr.trentu.ca/myAccount/aptbooking/internationalprogramappt.htm", \
            description="Click here to book an appointment with Trent International")
        await ctx.send(embed=embed)

    @book.command()
    async def career(self, ctx):
        embed=discord.Embed(title="Careerspace", color=0x3a8d34, url="https://ccr.trentu.ca/myAccount/aptbooking/ccappointments.htm", \
            description="Click here to book an appointment with Careerspace")
        await ctx.send(embed=embed)

    @book.command()
    async def peer(self, ctx):
        embed=discord.Embed(title="Peer Support", color=0x3a8d34, url="https://ccr.trentu.ca/myAccount/aptbooking/PeerSupport.htm", \
            description="Click here to book an appointment with a Peer Supporter")
        await ctx.send(embed=embed)

    @book.command()
    async def coop(self, ctx):
        embed=discord.Embed(title="Co-Op", color=0x3a8d34, url="https://ccr.trentu.ca/myAccount/aptbooking/co-op-appointments.htm", \
            description="Click here to book an appointment with your Co-Op Coordinator")
        await ctx.send(embed=embed)

#Required to add the functions
async def setup(bot):
    await bot.add_cog(Booking(bot))