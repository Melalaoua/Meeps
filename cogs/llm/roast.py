import discord
from discord.ext import commands

from features.commons import discord_msg, llm_interact


class roast_cmd(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.db_pool = self.bot.db_pool
    

    @commands.command(name="roast")
    async def roast(self, ctx, member:discord.Member = None) -> None:
        """Use openAI chatGPT3.5 to roast a user using his latest message sent in the server

        Args:
            ctx (discord.context)
            member (discord.Member, optional): User member mention in the discord message. Defaults to None.
        """
        if not member:
            await ctx.send("Précise une cible connard")
        
        async with ctx.typing():
            user_messages = await discord_msg.fetch_user_message(self.db_pool, member.id)
            
            if not user_messages:
                await ctx.send(f"{member.mention} a envoyé 0 message, tu veux que je le roast sur quoi au juste ?")
                return
            
            # Combine last 40 messages or less
            messages = "\n".join(user_messages[:30])
            roast = await llm_interact.roast_gpt(member.name, messages)
            
        await ctx.send(roast["choices"][0]["text"])   
    
    @commands.command(name="love")
    async def roast(self, ctx, member:discord.Member = None) -> None:
        """Use openAI chatGPT3.5 to compliment a user using his latest message sent in the server

        Args:
            ctx (discord.context)
            member (discord.Member, optional): User member mention in the discord message. Defaults to None.
        """
        if not member:
            await ctx.send("Précise une cible connard")
        
        async with ctx.typing():
            user_messages = await discord_msg.fetch_user_message(self.db_pool, member.id)
            
            if not user_messages:
                await ctx.send(f"{member.mention} a envoyé 0 message, tu veux que je jute sur quoi au juste ?")
                return
            
            # Combine last 40 messages or less
            messages = "\n".join(user_messages[:30])
            roast = await llm_interact.love_gpt(member.name, messages)
            
        await ctx.send(roast["choices"][0]["text"])  
        
        

async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(roast_cmd(bot))
