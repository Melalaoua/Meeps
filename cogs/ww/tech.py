import discord
from discord.ext import commands,tasks

from features.commons import scrape, common

import asyncio


class tech(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.web_client = self.bot.web_client
        self.search_new_post.start()
        self.db_pool = self.bot.db_pool
        self.browser = self.bot.browser
        self.scraping_list = scrape.fetch_scraping_list("technology")
        self.cat_color = "0x219ebc"
        
    def cog_unload(self):
        self.search_new_post.cancel()

    @tasks.loop(minutes=30)
    async def search_new_post(self):
        
        guild = self.bot.get_guild(212342095401320448)
        if not guild:
            return
        
        for scrape_name, data in self.scraping_list.items():
            data = await scrape.scrape_handler(self.web_client, self.db_pool, self.browser, scrape_name, data, guild, self.cat_color, cat_name="Tech")

            self.scraping_list[scrape_name] = data
            waiting_time = common.rand_number()
            await asyncio.sleep(waiting_time)


async def setup(bot = commands.Bot) -> None:
    await bot.add_cog(tech(bot))

# "immunology":{
#                         "channel" : 1105367319112318997,
#                         "thread" : false,
#                         "websites" :
#                     },
#                     "science_news":{
#                         "channel" : 1105367319112318997,
#                         "thread" : false,
#                         "websites" :
#                     },
#                     "science_reviews":{
#                         "channel" : 1105367319112318997,
#                         "thread" : false,
#                         "websites" :
#                     }



