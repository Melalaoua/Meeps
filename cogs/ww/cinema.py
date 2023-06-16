import discord
from discord.ext import commands,tasks



from bs4 import BeautifulSoup
from aiohttp import ClientSession

import favicon
import datetime


utc = datetime.timezone.utc
# If no tzinfo is given then UTC is assumed.
time = datetime.time(hour=6, minute=30, tzinfo=utc)


class cinema(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.web_client = self.bot.web_client
        self.sorties.cancel()

    def cog_unload(self):
        self.sorties.stop()

    @tasks.loop(time=time)
    async def sorties(self):
        current_weekday = datetime.datetime.today().weekday()

        if current_weekday != 2 :
            return
        
        guild = self.bot.get_guild(212342095401320448)
        if not guild:
            return
        
        channel = guild.get_channel_or_thread(1105805934766346290)

        scraping_url = "https://www.senscritique.com/films/cette-semaine"
        icons = favicon.get(scraping_url)
        favicon_url = icons[0].url

        limit = 5

        async with self.web_client.get(scraping_url) as resp:
            body = await resp.text()
            soup = BeautifulSoup(body, "html.parser")

            main_div = soup.find("div", {"class" : "NextReleases__WrapperLists-sc-1ymgy8c-4 iIfHSF"})
            next_releases = main_div.find_all("div", {"class": "ProductListItem__Container-sc-1jkxxpj-0 btjqXG"})

            for index, movie in enumerate(next_releases):
                if index == limit :
                    break

                title = movie.find("h2").text
                eng_title = movie.find("p").text

                synopsis = movie.find("p", {"data-testid" : "synopsis"}).text
                other_info = movie.find("p", {"data-testid" : "other-infos"}).text
                creator = movie.find("p", {"data-testid" : "creators"}).text

                image_no_script = movie.find("noscript")
                image_url = image_no_script.find("img")["src"]

            
                embed=discord.Embed(title=title, description=f"*{eng_title}* \n {other_info}", color = 0x252525)
                embed.set_image(url=image_url)
                embed.add_field(name="Synopsis", value=synopsis)
                embed.set_footer(text=f"{creator}", icon_url=favicon_url)

                await channel.send(embed=embed)
            


async def setup(bot = commands.Bot) -> None:
    await bot.add_cog(cinema(bot))


