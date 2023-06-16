import discord
from discord.ext import commands,tasks

from features.commons import scrape

class cinema(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.web_client = self.bot.web_client
        self.search_game_news.start()
        self.scraping_list = scrape.fetch_scraping_list("Art")
        
        

    @tasks.loop(minutes = 8)
    async def search_game_news(self):
        
        guild = self.bot.get_guild(212342095401320448)
        if not guild:
            return
        
        for scrape_name, data in self.scraping_list.items():
            text_channel, scrape_data = data
            
            text_channel_n, text_channel_id = text_channel
            channel = guild.get_channel_or_thread(text_channel_id)

            if not channel:
                return
            
            scraped, article_embed, new_scrape_data, scrape_name  = await scrape.get_latest_news(self.web_client, scrape_data, scrape_name)
            
            if scraped:
                await channel.send(embed=article_embed)
                self.scraping_list[scrape_name] = (text_channel,new_scrape_data)
            else:
                return


async def setup(bot = commands.Bot) -> None:
    await bot.add_cog(cinema(bot))

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



