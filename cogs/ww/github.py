import discord
from discord.ext import commands,tasks 

from features.commons import scrape, common

import asyncio


class github(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.web_client = self.bot.web_client
        self.get_repository.start()
        self.previous_key = 0

    def cog_unload(self):
        self.get_repository.cancel()

    @tasks.loop(minutes=25)
    async def get_repository(self):
        scraped = False
        guild = self.bot.get_guild(212342095401320448)
        if not guild:
            return
        
        
        channel = guild.get_channel_or_thread(1106145146862587924)
        if not channel:
            return
        
        try:
            scraped, article_embed, scrape_key  = await scrape.get_repository(self.web_client, self.previous_key)
        except Exception as e :
                await channel.send(f'**`ERROR - Github :`** {type(e).__name__} - {e}')    

        
        if scraped:
            await channel.send(embed=article_embed)
            self.previous_key = scrape_key
            

        waiting_time = common.rand_number()
        await asyncio.sleep(waiting_time)
        


async def setup(bot = commands.Bot) -> None:
    await bot.add_cog(github(bot))