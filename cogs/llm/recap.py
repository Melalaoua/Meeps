import discord
from discord.ext import commands, tasks

from features.commons import scrape, scrape_sql, llm_interact, discord_msg

import datetime
utc = datetime.timezone.utc

time = datetime.time(hour=19, minute = 10, tzinfo=utc)

class recap(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.db_pool = self.bot.db_pool
        self.recap.start()
    
    def cog_unload(self):
        self.recap.stop()

    @tasks.loop(time=time)
    async def recap(self):
        """Get news scraped today by Meeps in various website (see cogs/ww/) and make a summary of all this using GPT3.5
        """
        guild = self.bot.get_guild(212342095401320448)
        channel = guild.get_channel_or_thread(1118230104112369674)

        all_news = await scrape_sql.fetch_top_news(self.db_pool)
        full_list = ""
        for id, content in all_news.items():
            full_list = full_list + content

        chat, persona_name, persona = await llm_interact.generate_prompt_journal(news_list = full_list)
        title = await llm_interact.prompt_gpt(chat, chat = True, max_tokens = 200)
        title = title['choices'][0]['message']['content']

        chat = await llm_interact.generate_prompt_journal(first = False, persona = persona, chat = chat, assistant_answer = title)
        summary = await llm_interact.prompt_gpt(chat, chat=True, max_tokens = 2000)
        summary = summary['choices'][0]['message']['content']
        

        await channel.send(title)

        if len(summary) > 1999:
            n = 1999
            chunks = [summary[i:i+n] for i in range(0, len(summary), n)]
            for chunk in chunks :
                await channel.send(chunk)
        else:
            await channel.send(summary)
    

    @commands.command(name="tldr")
    async def tldr(self, ctx) -> None:
        """Make a summary of the latest message send in the channel using GPT 3.5

        Args:
            ctx (discord.context)
        """
      
        async with ctx.typing():
            channel_id = ctx.message.channel.id
            messages = await discord_msg.fetch_latest_message(self.db_pool, channel_id)

            if not messages:
                await ctx.send("Il y a une erreur, je n'arrive pas à accéder aux derniers messages")
                return
            
            # Combine last 40 messages or less
            llm_prompt = "En te basant sur les messages d'une conversation bien trop longue pour que je la lise, fais moi un résumé concis et précis de ce qui a été dit dans cette conversation, voici les messages :"
            llm_prompt = f"{llm_prompt}\n".join(messages[:20])
             
            answer= await llm_interact.prompt_gpt(llm_prompt)
            
        await ctx.send(answer["choices"][0]["text"])   
        
        

async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(recap(bot))
