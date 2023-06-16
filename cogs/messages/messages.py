import discord
from discord.ext import commands

from features.commons import discord_msg,user_info, milestone_handler


class message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_pool = self.bot.db_pool
        self.users_dict = self.bot.users_dict
        self.channels_dict = self.bot.channels_dict

    @commands.Cog.listener()
    async def on_message(self, message):
        """When a message is sent in the discord, load message in database

        Args:
            message (discord.message)
        """

        chunk_size, message_crate, user_message_aload_crate, channel_message_aload_crate = await discord_msg.message_fetch(message)
        user_crate = await discord_msg.user_fetch(message, self.users_dict)
        channel = message.channel

        channel_crate = await discord_msg.channel_fetch(channel, self.channels_dict)
        

        await discord_msg.channel_loader(self.db_pool, channel_crate)
        await discord_msg.user_loader(self.db_pool, user_crate)
        await discord_msg.message_loader(self.db_pool, message_crate)

        await discord_msg.channel_message_aloader(self.db_pool, channel_message_aload_crate)
        await discord_msg.user_message_aloader(self.db_pool, user_message_aload_crate)

        user_id = message.author.id

        message_count = await user_info.fetch_user(self.db_pool, user_id, is_message = True)
        table_info_message = "T''écrit bcp Machallah%"
        await milestone_handler.check_milestone(self.bot, self.db_pool, user_id, table_info_message, message_count, message)
    

            





async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(message(bot))
