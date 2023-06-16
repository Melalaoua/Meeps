import discord
from discord.ext import commands

from features.commons import milestone_handler

class milestone_pagination(discord.ui.View):
    """Pagination, the detail of each function is already explained in cogs/common/book.py

    This pagination send all the milestone of the server, show user's progress
    """
    current_page: int = 1
    sep : int = 1

    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep])
    
    def create_embed(self, data):
        for categories in data:
            for category, milestones in categories.items():
                embed = discord.Embed(title=category)
                for milestone in milestones:
                    milestone_desc = f"{milestone[1]} \n"
                    if milestone[2]:
                        milestone_reward = f"__{milestone[2]}__\n"
                    else:
                        milestone_reward=None

                    milestone_laureum = f"**╰ {milestone[3]} laureum** \n"
                    divider = "‎‎‎‎"
                
                    if milestone[4]:
                        date = milestone[4].strftime("%Y/%m/%d")
                        completed = f"\n *Complété le {date}* \n "
                    else:
                        completed = False

                    if milestone_reward:
                        field_value = milestone_desc +  milestone_laureum + milestone_reward + divider
                    else:
                        field_value = milestone_desc + milestone_laureum + divider
                    
                    if completed:
                        field_value = field_value + completed + divider
                    embed.add_field(name=f"{milestone[0]}", value=field_value, inline=True)

            return embed

    async def update_message(self, data):
        self.update_buttons()
        await self.message.edit(embed=self.create_embed(data), view=self)

    def update_buttons(self):
        if self.current_page == 1:
            self.first_page_button.disabled = True
            self.first_page_button.style = discord.ButtonStyle.gray
            self.prev_button.disabled = True
            self.prev_button.style = discord.ButtonStyle.gray
        else:
            self.first_page_button.disabled = False
            self.first_page_button.style = discord.ButtonStyle.green
            self.prev_button.disabled = False
            self.prev_button.style = discord.ButtonStyle.primary
        if self.current_page == int(len(self.data) / self.sep) + 1:
            self.next_button.disabled = True
            self.next_button.style = discord.ButtonStyle.gray
            self.last_page_button.disabled = True
            self.last_page_button.style = discord.ButtonStyle.gray
        else:
            self.next_button.disabled = False
            self.next_button.style = discord.ButtonStyle.primary
            self.last_page_button.disabled = False
            self.last_page_button.style = discord.ButtonStyle.green


    @discord.ui.button(label="⋘", style=discord.ButtonStyle.green)
    async def first_page_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
        self.current_page = 1
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        await self.update_message(self.data[:until_item])

    @discord.ui.button(label="⋖", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
        self.current_page -= 1
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        await self.update_message(self.data[from_item:until_item])



    @discord.ui.button(label="⋗", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
        self.current_page += 1
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        await self.update_message(self.data[from_item:until_item])

    @discord.ui.button(label="⋙", style=discord.ButtonStyle.green)
    async def last_page_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
        self.current_page = int(len(self.data)/self.sep) + 1
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        await self.update_message(self.data[from_item:])


class milestone(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_pool = self.bot.db_pool
    
    @commands.command()
    async def milestone(self, ctx):
        user_id = ctx.message.author.id
        data = await milestone_handler.fetch_all_milestone(self.db_pool, user_id)
        pagination_view=milestone_pagination()
        pagination_view.data = data
        await pagination_view.send(ctx)
        



async def setup(bot:commands.Bot)->None:
    await bot.add_cog(milestone(bot))