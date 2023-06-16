import discord
from discord.ext import commands


from features.commons import user_info, milestone_handler


class milestone_message_archive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_pool = self.bot.db_pool


    
    @commands.command(name="ma")
    @commands.is_owner()
    async def milestone_archive(self, ctx):
        """This command is to catch-up the success system using database's data. Get user message, and other's command metrics to attribute success (milestones)

        Args:
            ctx (discord.Context)
        """

        table_info_message = "T''écrit bcp Machallah%"
        table_info_fart_1 = "Cacaphonie%" 
        table_info_fart_2 = "L''ami des pets%" 
        table_info_pdm_1 = "Daronne en vue !%"
        table_info_pdm_2 = "La daronne de trop%"
        milestones_message_dict = await milestone_handler.fetch_milestone(self.db_pool, table_info_message)
        milestones_fart_dict_1 = await milestone_handler.fetch_milestone(self.db_pool, table_info_fart_1)
        milestones_fart_dict_2 = await milestone_handler.fetch_milestone(self.db_pool, table_info_fart_2)
        milestones_pdm_dict_1 = await milestone_handler.fetch_milestone(self.db_pool, table_info_pdm_1)
        milestones_pdm_dict_2 = await milestone_handler.fetch_milestone(self.db_pool, table_info_pdm_2)
        
        async for member in ctx.guild.fetch_members(limit=None):
            if member.bot :
                continue
        
            else:
                user_id = member.id
                message = ctx.message
                
                message_count, fart_count_e, fart_count_r, pdm_count_e, pdm_count_r = await user_info.fetch_user(self.db_pool, user_id, is_milestone=True)
                
                await milestone_handler.is_milestone_completed(self.bot, self.db_pool, milestones_message_dict, user_id, message_count, message)
                await milestone_handler.is_milestone_completed(self.bot, self.db_pool, milestones_fart_dict_1, user_id, fart_count_e, message)
                await milestone_handler.is_milestone_completed(self.bot, self.db_pool, milestones_fart_dict_2, user_id, fart_count_r, message)
                await milestone_handler.is_milestone_completed(self.bot, self.db_pool, milestones_pdm_dict_1, user_id, pdm_count_e, message)
                await milestone_handler.is_milestone_completed(self.bot, self.db_pool, milestones_pdm_dict_2, user_id, pdm_count_r, message)
        
        await role_distribution(self.db_pool, ctx)

      


async def role_distribution(db_pool, ctx):
    connection = await db_pool.acquire()
    async with connection.transaction():
        query="select moodyblues.user.discord_id, title.discord_id as role_id from moodyblues.user INNER JOIN user_title ON user_title.user_id=moodyblues.user.id INNER JOIN milestones.title ON user_title.title_id=title.id;"

        result = await db_pool.fetch(query)
        
        result = [dict(row) for row in result]
        
    await db_pool.release(connection)

    role_attribution_dict = {}
    for title in result:
        user_id = title["discord_id"]
        role_id = title["role_id"]

        if user_id in role_attribution_dict:
            role_id_list = role_attribution_dict[user_id]
            role_id_list.append(role_id)
            role_attribution_dict[user_id] = role_id_list
        else:
            role_attribution_dict[user_id] = [role_id]

        for user_id, role_id_list in role_attribution_dict.items():
            member = await ctx.guild.fetch_member(user_id)
            role_object_list=[]
            for role_id in role_id_list:
                
                role = ctx.guild.get_role(role_id)
                role_object_list.append(role)

            await member.add_roles(*role_object_list)



async def setup(bot:commands.Bot)-> None:
    await bot.add_cog(milestone_message_archive(bot))




# On Hold  
# async def role_creation(db_pool, guild, bot):
#     connection=await db_pool.acquire()
#     async with connection.transaction():
#         query="SELECT title from milestones.title;"

#         result = await db_pool.fetch(query)
        
#         result = [dict(row) for row in result]

#         title_list=[]
#         for title in result:
#             title_list.append(title["title"])
        
#     await db_pool.release(connection)
    
#     for title in title_list:
#         await bot.guild.create_role(name=title, )