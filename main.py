import nextcord 
from nextcord.ext import commands 
from links import TOKEN, API_KEY
import aiohttp

#Sets up basic configurations for the bot 
bot = commands.Bot(command_prefix="!", intents = nextcord.Intents.all())

#Loads the Helper Cog function to print the help commands
bot.load_extension("helperCog")

@bot.event
async def on_ready():
    print("Weather Bot has connected to Discord")

#Bot Command to get the current weather of a city or location
@bot.command() 
async def weather(ctx: commands.Context, *, city):
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": API_KEY,
        "q": city
    }

    async with aiohttp.ClientSession() as session: 
        async with session.get(url, params=params) as res: 
            data = await res.json()

            location = data["location"]["name"]
            temp_c = data["current"]["temp_c"]
            temp_f = data["current"]["temp_f"]
            humidity = data["current"]["humidity"]
            wind_kph = data["current"]["wind_kph"]
            wind_mph = data["current"]["wind_mph"]
            gust_mph = data["current"]["gust_mph"]
            gust_kph = data ["current"]["gust_kph"]
            precip = data["current"]["precip_in"]
            condition = data["current"]["condition"]["text"]
            image_url = "http:" + data["current"]["condition"]["icon"]

            embed = nextcord.Embed(title=f"Weather for {location}", description=f"The condition for '{location}' is '{condition}'")
            embed.add_field(name="Temperature", value=f"Celsius: {temp_c} | Fahrenheit: {temp_f}")
            embed.add_field(name="Humidity", value=f"{humidity}")
            embed.add_field(name="Precipitation", value=f"{precip}")
            embed.add_field(name="Gust Speed", value=f"KPH: {gust_kph} | MPH: {gust_mph}")
            embed.add_field(name="Wind Speeds", value=f"KPH: {wind_kph} | MPH: {wind_mph}")
            embed.set_thumbnail(url=image_url)

            await ctx.send(embed=embed)

#Bot Command to get the forecast of a city or location for the next 7 days 
@bot.command() 
async def forecast(ctx: commands.Context, *, city ):
    url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": API_KEY,
        "q": city,
        "days": 7
    } 

    async with aiohttp.ClientSession() as session: 
        async with session.get(url, params=params) as res:
            data = await res.json()

            forecast_days = data["forecast"]["forecastday"]

            for day_data in forecast_days:
                date = day_data["date"]
                condition = day_data["day"]["condition"]["text"]
                max_tempC = day_data["day"]["maxtemp_c"]
                max_tempF = day_data["day"]["maxtemp_f"]
                min_tempC = day_data["day"]["mintemp_c"]
                min_tempF = day_data["day"]["mintemp_f"]
                image_url = "http:" + day_data["day"]["condition"]["icon"]
                
                embed = nextcord.Embed(title=f"Forecast for {date}")
                embed.add_field(name="Condition", value=f"{condition}")
                embed.add_field(name="Max Temperature", value=f"Celsius{max_tempC} | Fahrenheit:{max_tempF}")
                embed.add_field(name="Min Temperature", value=f"Celsius{min_tempC} | Fahrenheit:{min_tempF}")
                embed.set_thumbnail(url=image_url)
                
                await ctx.send(embed=embed)


bot.run(TOKEN)