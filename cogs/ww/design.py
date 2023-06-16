import discord
from discord.ext import commands,tasks

from features.commons import scrape, common
import asyncio


class design(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.web_client = self.bot.web_client
        self.db_pool = self.bot.db_pool
        self.browser = self.bot.browser
        self.search_new_post.start()
        self.scraping_list = scrape.fetch_scraping_list("design")
        self.cat_color = "0xFFD670"

    def cog_unload(self):
        self.search_new_post.cancel()     
    
    @tasks.loop(minutes=25)
    async def search_new_post(self):
        
        guild = self.bot.get_guild(212342095401320448)
        if not guild:
            return
        
        for scrape_name, data in self.scraping_list.items():
            data = await scrape.scrape_handler(self.web_client, self.db_pool, self.browser, scrape_name, data, guild, self.cat_color, cat_name="Design")

            self.scraping_list[scrape_name] = data
            waiting_time = common.rand_number()
            await asyncio.sleep(waiting_time)



async def setup(bot = commands.Bot) -> None:
    await bot.add_cog(design(bot))
