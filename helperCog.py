import nextcord
from nextcord.ext import commands

class helper_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #Override the default help command 
        bot.remove_command("help")    

    @commands.command()
    async def help(self, ctx):
        help_message = """

        General commands:
        !help - Displays all the available commands in this Weather Bot  
        !weather {city/state/country} - Displays the temperature, humidity, preciptation levels, gust speed and wind speed of the specificed location
        !forecast {city/state/country} - Displays the forecast for the next 7 days of the specified locaiton
        """

        embed = nextcord.Embed(title="Weather Bot Help", description=help_message, color=0x0000FF)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(helper_cog(bot))