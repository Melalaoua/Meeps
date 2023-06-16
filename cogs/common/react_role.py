import discord
from discord.ext import commands

from Meeps import cu

class react_role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.role_message_id = 1108851306757628014  # ID of the message that can be reacted to to add/remove a role.
        self.emoji_to_role = {
            discord.PartialEmoji(name='🌍'): 1106847587010621570,  # ID of the role associated with unicode emoji '🔴'.
            discord.PartialEmoji(name='👾'): 1106847775355850803,
            # discord.PartialEmoji(name='🎬'): 1106847857513869373,
            # discord.PartialEmoji(name='🎵'): 1106847930654138448,
            discord.PartialEmoji(name='🧪'): 1106848047259996200,
            discord.PartialEmoji(name='🤖'): 1106848208468062218,
            discord.PartialEmoji(name='👹'): 1106848319730368542,
            # discord.PartialEmoji(name='🍳'): 1106851595913793597,
            discord.PartialEmoji(name='🌴'): 1110113864584011816,  # ID of the role associated with unicode emoji '🟡'.
            # discord.PartialEmoji(name='green', id=0): 0,  # ID of the role associated with a partial emoji's ID.
        }

    @commands.is_owner()
    @commands.command(name="send_embed")
    async def send_news_embed_role(self, ctx):
        """Send embed with various description that user must react to in order to get a specific role. Emoji are linked to specific role id inside the guild.

        Args:
            ctx (discord.context): context
        """
        embed= discord.Embed(title="🔮 Choose 🔮", description=" Quels types de news vous souhaitez suivre ? Réagissez avec un emoji afin d'avoir un accès direct au channels.", color=cu["color_patch_note"])
        embed.add_field(name="🌍 International", value="Actualité internationale, en Anglais/Francais.", inline=False)
        embed.add_field(name="👾 Gaming", value="Autour des jeux vidéos, grandes annonces et patchs de LoL", inline=False)
        # embed.add_field(name="🎬 Cinéma", value="Les films à l'affiche cette semaine, chaque mercredi à 8h30", inline=False)
        # embed.add_field(name="🎵 Musique [Prochainement]", value="Les prochains albums, musiques et grands events.", inline=False)
        embed.add_field(name="🧪 Scientifique", value="Les derniers papiers publiés de Nature, Science, ... Mais aussi quelques acutalités insolites et compréhensibles de tous.", inline=False)
        embed.add_field(name="🤖 Tech", value="Principalement autour des IAs, les grandes sorties de la techs.", inline=False)
        embed.add_field(name="👹 Manga", value="Les prochains animes à venir, informations diverses.", inline=False)
        # embed.add_field(name="🍳 Cuisine [Prochainement]", value="Recettes de cuisines.", inline=False)
        embed.add_field(name="🌴 Treasure Trove", value="Toutes les trouvailles utiles sur internet, des sites webs, des IAs, des offres de réduction.", inline=False)
        
        old_embed_id = 1108851306757628014
        # old_embed_id = False
        if old_embed_id :
            old_embed = await ctx.channel.fetch_message(old_embed_id)
            if old_embed:
                message = await old_embed.edit(embed=embed)
        else:
            message = await ctx.send(embed=embed)

        await message.add_reaction("🌍")
        await message.add_reaction("👾")
        # await message.add_reaction("🎬")
        # await message.add_reaction("🎵")
        await message.add_reaction("🧪")
        await message.add_reaction("🤖")
        await message.add_reaction("👹")
        # await message.add_reaction("🍳")
        await message.add_reaction("🌴")
    

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload:discord.RawReactionActionEvent):
        """When reaction is added on the discord message (id stored), if emoji matches, add role to user. 
        Args:
            payload (discord.RawReactionActionEvent): reaction event
        """
        if payload.message_id != self.role_message_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            return

        role = guild.get_role(role_id)
        if role is None:
            return

        try :
            await payload.member.add_roles(role)

        except discord.HTTPException:
            pass
    
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload:discord.RawReactionActionEvent):
        """When reaction is removed on the discord message (id stored), if emoji matches, remove role to user. 
        Args:
            payload (discord.RawReactionActionEvent): reaction event
        """
        if payload.message_id != self.role_message_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            return

        role = guild.get_role(role_id)
        if role is None:
            return


        member = guild.get_member(payload.user_id)
        if member is None:
            return
        
        try :
            await member.remove_roles(role)

        except discord.HTTPException:
            pass
    

async def setup(bot:commands.Bot) -> None :
    await bot.add_cog(react_role(bot))