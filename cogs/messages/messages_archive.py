import discord
from discord.ext import commands
import time

from features.commons import discord_msg



class messages_archives(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_pool = self.bot.db_pool
        self.users_dict = self.bot.users_dict
        self.channels_dict = self.bot.channels_dict

    @commands.command()
    @commands.is_owner()
    async def sweep(self, ctx):
        await ctx.channel.send("Je m'en occupe.")
        """Fetch all message of the server to include the inside the postgresql database, this process can take a very long time for big servers.
        """
        
        # Loads
        user_load = []
        channel_load = []
        message_load = []
        
        # aLoads
        user_message_aload = []
        channel_message_aload = []


        #chunk definition
        chunk_size = 0
        chunk_limit = 50000
        message_cargo = {}

        user_message_acargo = {}
        channel_message_acargo = {}

        # Loop through channels
        for channel in ctx.guild.text_channels:
            # Channel factory
            
            channel_crate = await discord_msg.channel_fetch(channel, self.channels_dict)
            if channel_crate:
                channel_load.append(channel_crate)

            messages_ids = await discord_msg.message_dict(self.db_pool)
            # Loop through messages
            async for message in channel.history(limit=None):   
                    
                # User factory
                if not message.id in messages_ids:
                    user_crate = await discord_msg.user_fetch(message, self.users_dict)
                    if user_crate:
                        user_load.append(user_crate)


                    # Message factory
                    chunk_size, message_crate, user_message_aload_crate, channel_message_aload_crate = await discord_msg.message_fetch(message, chunk_size)
                    message_load.append(message_crate)
                    user_message_aload.append(user_message_aload_crate)
                    channel_message_aload.append(channel_message_aload_crate)

                    
                    if chunk_size >= chunk_limit:
                        chunk_limit += 50000
                        cargo_id = str(f"cargo_{chunk_size}_{chunk_limit}")
                        message_cargo[cargo_id] = message_load
                        message_load=[]

                        user_message_acargo[cargo_id]=user_message_aload
                        user_message_aload=[]

                        channel_message_acargo[cargo_id]=channel_message_aload
                        channel_message_aload=[]
                        
                else:
                    continue
        
        
        if message_load:
            cargo_id="cargo_remnants"
            message_cargo[cargo_id] = message_load
            message_load=[]

            user_message_acargo[cargo_id]=user_message_aload
            user_message_aload=[]

            channel_message_acargo[cargo_id]=channel_message_aload
            channel_message_aload=[]


        await discord_msg.channel_loader(self.db_pool, channel_load)
        await discord_msg.user_loader(self.db_pool, user_load)
        
        time.sleep(10)

        for cargo_id in message_cargo:
            message_load = message_cargo[cargo_id]
            await discord_msg.message_loader(self.db_pool, message_load)
        
        for cargo_id in user_message_acargo:
            user_message_aload = user_message_acargo[cargo_id]
            await discord_msg.user_message_aloader(self.db_pool, user_message_aload)
        
        for cargo_id in channel_message_acargo:
            channel_message_aload = channel_message_acargo[cargo_id]
            await discord_msg.channel_message_aloader(self.db_pool, channel_message_aload)
    

        await ctx.channel.send("C'est fait.")



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(messages_archives(bot))


