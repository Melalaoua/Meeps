import discord
from discord.ext import commands

from features.commons import user_info, common
from Meeps import embed_guidelines,cu


class title_dropdown(discord.ui.Select):
    """Show user's title obtained through milestone success. When a title is selected, it is shown in other command's (e.g user_info)

    Args:
        discord (discord.ui.Select)
    """
    def __init__(
            self, 
            titles,
            db_pool,
            author
    ):
        self.titles = titles
        self.db_pool = db_pool
        self.author = author

        
        options = []
        # Set the options that will be presented inside the dropdown
        for title,ids in titles.items():
            option = discord.SelectOption(label=title)
            options.append(option)
        
        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder="Choississez le titre que vous souhaitez porter", min_values=1, max_values=1, options=options)
    

    async def callback(self, interaction:discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        if interaction.user.id == self.author.id:
            await interaction.response.send_message(f"Vous portez maintenant le titre *{self.values[0]}*", ephemeral = True)
            chosen_title = self.values[0]
            ids = self.titles[chosen_title]

            connection = await self.db_pool.acquire()
            async with connection.transaction():
                query = "UPDATE user_title set active=False where user_id =$1;"
                await self.db_pool.execute(query, ids[0])

                query = "UPDATE user_title set active=True where user_id =$1 AND title_id=$2;"
                await self.db_pool.execute(query, *ids)

            await self.db_pool.release(connection)
        else:
            await interaction.response.send_message(f"Qui es-tu pour te faire passer pour {self.author.name} ?")
    
    



class DropdownView(discord.ui.View):
    def __init__(
            self,
            titles,
            db_pool,
            author
    ):
        self.titles = titles
        self.db_pool = db_pool
        self.author = author
        super().__init__()

        self.add_item(title_dropdown(titles = self.titles, db_pool=self.db_pool, author=self.author))
        



class title_selector(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_pool = self.bot.db_pool
        

    @commands.command()
    async def titres(self, ctx, member:discord.Member=None):
        
        if not member:
            message = ctx.message
            title_dict_clean, no_title = await user_info.fetch_titles(self.db_pool, message.author.id)
            
            if no_title:
                await ctx.send("Vous n'avez pas de titre")
            else:
                view = DropdownView(titles=title_dict_clean, db_pool=self.db_pool, author = ctx.message.author)
                await ctx.send('Choisissez votre titre :', view=view)
        
        else:
            if member.id == ctx.message.author.id:
                title_dict_clean, no_title = await user_info.fetch_titles(self.db_pool, ctx.message.author.id)

                if no_title:
                    await ctx.send("Vous n'avez pas de titre")
                else:
                    view = DropdownView(titles=title_dict_clean, db_pool=self.db_pool, author = ctx.message.author)
                    await ctx.send('Choisissez votre titre :', view=view)
            else:
                title_dict_clean, no_title = await user_info.fetch_titles(self.db_pool, member.id)
                
                if no_title:
                    await ctx.send("L'utilisateur ne possède pas de titre")
                else:
                    embed = discord.Embed(title=f"Titre de {member.name}", color=embed_guidelines['color'])
                    
                    title_str_list=""
                    
                    for title, ids in title_dict_clean.items():
                        title_str_list = f"{title_str_list} *{title}* \n"
                    
                    embed.add_field(name="", value=title_str_list)

                    update = cu["update"]
                    time = common.get_time()
                    embed.set_footer(text=f"{time} - Meeps - patch {update}", icon_url=ctx.guild.icon)
                    
                    await ctx.channel.send(embed=embed)
                    



async def setup(bot:commands.Bot)->None:
    await bot.add_cog(title_selector(bot))