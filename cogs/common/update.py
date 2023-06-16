import discord
from discord.ext import commands

from Meeps import embed_guidelines, cu, pn
from features.commons import common 

class update(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.release_date = cu["release_date"]
        self.update_name = cu["update"]

    @commands.command(name="update")
    async def update(self, ctx):
        """Send discord embed containing data on the current Meeps update. Data on the current update are stored inside the init.py

        Args:
            ctx (_type_): _description_
        """
        update_desc = cu["update_description"]
        update_embed = discord.Embed(title="🧙‍♂️ Ouverture du Quartier des Mages 🧙‍♂️", color=cu["color_update"], description=f"Meeps tourne actuellement sous l'update **{self.update_name}**, sortie le *{self.release_date}*.\n {update_desc}")

        
        for function, detail in cu["whats_new"].items():
            update_embed.add_field(name=function, value=detail, inline=False)

        update_embed.set_image(url="attachment://banner.png")
        banner = discord.File(cu["banner"], filename="banner.png")
        
        await ctx.send(file=banner, embed=update_embed)
        banner.close()

    
    @commands.command(name="patch")
    async def patch_note(self, ctx):
        """Send latest patch/hotfix of Meeps

        Args:
            ctx (discord.context)       
        """
        
        patch_embed = discord.Embed(title=f"{cu['update']}-{pn['name']}", color=cu["color_patch_note"], description=pn['desc'])  
        patch_embed.add_field(name=" 🔺 ```AJOUTS```", value=pn["ajout_desc"])
        patch_embed.add_field(name=" ⚙️ ```MODIFICATIONS``` ", value=pn["modif_desc"], inline=False)
        
        time = common.get_time()
        patch = pn["release_date"]
        patch_embed.set_footer(text=f"{time} - Meeps - patch {patch}", icon_url=ctx.guild.icon)
        
        await ctx.send(embed=patch_embed)
        
            


async def setup(bot:commands.Bot)->None:
    await bot.add_cog(update(bot))