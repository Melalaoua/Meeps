import discord
from discord.ext import commands

from Meeps import embed_guidelines, cu
from features.commons import common, user_info

from datetime import datetime

class user(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_pool = self.bot.db_pool



    @commands.command(name="avatar")
    async def avatar(self, ctx, member:discord.Member = None) -> None:
        """Send user profile picture in the server or target's profile picture.

        Args:
            ctx (discord.Context)
            member (discord.Member, optional): Defaults to None.
        """
        
        message = ctx.message
        requested_by = None

        if not member :
            title_embed = message.author.name
            avatar = message.author.avatar
            embed = await avatar_embed_factory(title_embed, avatar, requested_by)
            

        elif member:
            title_embed = member.name
            avatar = member.avatar
            requested_by = message.author.name
            embed = await avatar_embed_factory(title_embed, avatar, requested_by)
        
        server_image = discord.File(embed_guidelines["server_image"], filename="server.png")
        await ctx.send(file = server_image, embed=embed)
        server_image.close()

        await message.delete()


    @commands.command(name="d")
    async def user_detail(self, ctx, member:discord.Member=None) -> None:
        """Show user discord's information or database's information (e.g number of message, join date, ...)

        Args:
            ctx (discord.Context)
            member (discord.Member, optional): Defaults to None.
        """
        message = ctx.message

        if not member:
            joined_at = message.author.joined_at.strftime("%d/%m/%Y")
            
            user_id = message.author.id
            message_count, fart_count, pdm_count = await user_info.fetch_user(self.db_pool, user_id)
            user_lauriers, total_lauriers = await user_info.fetch_laurier(self.db_pool, user_id)
            user_title = await user_info.fetch_active_title(self.db_pool, user_id)

            if user_title:
                title_value = f"{message.author.name}, {user_title}"

            else : 
                title_value = f"{message.author.name}"

            embed = discord.Embed(title = title_value, description=f"Membre depuis le : {joined_at}", color=embed_guidelines["color"])

            message_stat = f"‎‎‎︱ **📃 {message_count}** messages \n┆ \n"
            fart_stat = f"‎‎‎︱ **💩 {fart_count}** ifart\n┆ \n"
            pdm_stat = f"‎‎‎︱ **💃 {pdm_count}** iputedemere\n┆\n"
            lauriers = f"‎‎‎︱ **⚜️ {user_lauriers}** laureum \n\n"
            stat_desc = f"{message_stat}{fart_stat}{pdm_stat}{lauriers}"
            
            embed.add_field(name="Statistiques", value=f"{stat_desc}")

            time = common.get_time()
            update = cu["update"]

            embed.set_thumbnail(url=message.author.avatar)
        
        if member:
            if member.bot:
                await ctx.send("Vous ne pouvez pas cibler des bots")
                return
            
            else:
                joined_at = member.joined_at.strftime("%d/%m/%Y")
                user_id = member.id

                message_count, fart_count, pdm_count = await user_info.fetch_user(self.db_pool, user_id)
                user_lauriers, total_lauriers = await user_info.fetch_laurier(self.db_pool, user_id)
                user_title = await user_info.fetch_active_title(self.db_pool, user_id)

                if user_title:
                    title_value = f"{member.name}, {user_title}"
                else : 
                    title_value = f"{member.name}"

                embed = discord.Embed(title = title_value, description=f"Membre depuis le : {joined_at}", color=embed_guidelines["color"])

                message_stat = f"‎‎‎︱ **📃 {message_count}** messages \n┆ \n"
                fart_stat = f"‎‎‎︱ **💩 {fart_count}** ifart\n┆ \n"
                pdm_stat = f"‎‎‎︱ **💃 {pdm_count}** iputedemere\n┆\n"
                lauriers = f"‎‎‎︱ **⚜️ {user_lauriers}** laureum \n\n"
                stat_desc = f"{message_stat}{fart_stat}{pdm_stat}{lauriers}"
                
                embed.add_field(name="Statistiques", value=f"{stat_desc}")

                time = common.get_time()
                update = cu["update"]
            
                embed.set_thumbnail(url=member.avatar)

        
        embed.set_footer(text=f"{time} - Meeps - update {update}", icon_url="attachment://server.png")
        
        server_image = discord.File(embed_guidelines["server_image"], filename="server.png")
        await ctx.channel.send(file=server_image , embed=embed)
        server_image.close()



        
async def avatar_embed_factory(title_embed, avatar, requested_by):
    """Generate the embed to end the profile picture

    """
    
    embed = discord.Embed(colour = embed_guidelines["color"], title = title_embed)
    update = cu["update"]
    time = common.get_time()

    if requested_by :
        embed.set_footer(text=f"Demandé par {requested_by} - {time} - Meeps - patch {update}", icon_url="attachment://server.png")

    else:
        embed.set_footer(text=f"{time} - Meeps - patch {update}", icon_url="attachment://server.png")

    embed.set_image(url=avatar)

    return embed



async def setup(bot:commands.Bot)->None:
    await bot.add_cog(user(bot))