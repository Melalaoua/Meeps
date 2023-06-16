import discord
from discord.ext import commands

from features.commons import common

#https://github.com/richardschwabe/discord-bot-2022-course/blob/main/pagination.py

class PaginationView(discord.ui.View):
    """Handle the pagination of the embed in discord
    """
    
    current_page: int = 1
    sep : int = 5

    async def send(self, ctx):
        """Send embed"""
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep])
    
    def create_embed(self, data):
        """
        Initialize discord embed

        Args:
            data: content to put in embed
        """
        embed = discord.Embed(title="Commandes Meeps")
        for command_dict in data :
            for command_name, values in command_dict.items():
                command_desc = f"╰ {values[1]} \n"
                command_usage = f"`{values[2]}`\n"
                divider = "‎‎‎‎"
                embed_value = command_desc + command_usage + divider
                embed.add_field(name=f"{values[0]} {command_name}", value=embed_value, inline=False)
        return embed

    async def update_message(self, data):
        """When change page button clicked, update the message with the new embed.

        Args:
            data (list): new data contained with embed
        """
        self.update_buttons()
        await self.message.edit(embed=self.create_embed(data), view=self)

    def update_buttons(self):
        """Update label of button under embed
        """
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
        """Button for first page of the pagination embed

        Args:
            interaction (discord.Interaction): click action
            button (discord.ui.Button): id of the button
        """
        await interaction.response.defer()
        self.current_page = 1
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        await self.update_message(self.data[:until_item])

    @discord.ui.button(label="⋖", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        """Button for the previous page of the pagination embed. If the page 1, button disabled

        Args:
            interaction (discord.Interaction): 
            button (discord.ui.Button): 
        """
        await interaction.response.defer()
        self.current_page -= 1
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        await self.update_message(self.data[from_item:until_item])



    @discord.ui.button(label="⋗", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        """Next page of the pagination. If last page, button disabled

        Args:
            interaction (discord.Interaction): 
            button (discord.ui.Button): 
        """
        await interaction.response.defer()
        self.current_page += 1
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        await self.update_message(self.data[from_item:until_item])

    @discord.ui.button(label="⋙", style=discord.ButtonStyle.green)
    async def last_page_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        """Button to jump to last page of the pagination, if already last page, button disabled.
        """
        await interaction.response.defer()
        self.current_page = int(len(self.data)/self.sep) + 1
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        await self.update_message(self.data[from_item:])


class help_book(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  
    
    @commands.command()
    async def book(self, ctx):
        """Create a discord embed containing all the commands of Meeps stored on a json. The embed is subpoenaed with buttons bellow that update the embed and make it dynamic. The more commands exist on the bot ,the more page on the embed will be.

        Args:
            ctx (discord context): contain channel, guild, user, etc : see discord.py API doc for info
        """
        data = common.fetch_commands()
        pagination_view=PaginationView()
        pagination_view.data = data
        await pagination_view.send(ctx)
    
    








async def setup(bot:commands.Bot)->None:
    await bot.add_cog(help_book(bot))