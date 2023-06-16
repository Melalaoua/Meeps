import discord
from discord.ext import commands

from Meeps import cu
from features.commons import scrape_sql

class react_role_article(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_pool = self.bot.db_pool

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload:discord.RawReactionActionEvent):

        exist, scrape_id = await scrape_sql.scrape_score(self.db_pool, payload.message_id)

        if exist:
            if payload.emoji == discord.PartialEmoji(name='👍'):
                await scrape_sql.update_scrape_score(self.db_pool, scrape_id, add=True)
            
            elif payload.emoji == discord.PartialEmoji(name='👎'):
                await scrape_sql.update_scrape_score(self.db_pool, scrape_id, sub = True)
        
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload:discord.RawReactionActionEvent):
        exist, scrape_id = await scrape_sql.scrape_score(self.db_pool, payload.message_id)

        if exist:    
            if payload.emoji == discord.PartialEmoji(name='👍'):
                await scrape_sql.update_scrape_score(self.db_pool, scrape_id, sub=True)
            
            elif payload.emoji == discord.PartialEmoji(name='👎'):
                await scrape_sql.update_scrape_score(self.db_pool, scrape_id, add = True)

async def setup(bot:commands.Bot) -> None :
    await bot.add_cog(react_role_article(bot))