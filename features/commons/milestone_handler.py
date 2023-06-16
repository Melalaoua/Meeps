from datetime import datetime
import discord

import re
import pytz


from Meeps import embed_guidelines, cu
from features.commons import common

async def fetch_milestone(db_pool, table_info):
    connection = await db_pool.acquire()
    async with connection.transaction():
        query = f"SELECT * from milestones.milestone where title like '{table_info}';"

        result = await db_pool.fetch(query)
        raw_milestones_message_dict = [dict(row) for row in result]
        
        milestones_message_dict = {}
        for milestone_message_dict in raw_milestones_message_dict:
            milestones_message_dict[milestone_message_dict["id"]] = [milestone_message_dict["title"], milestone_message_dict["info"], milestone_message_dict["reward_desc"], milestone_message_dict["reward_lauriers"]]

    await db_pool.release(connection)
    return milestones_message_dict



async def fetch_user_milestone(db_pool, user_id):
    connection = await db_pool.acquire()
    async with connection.transaction():
        query = "select moodyblues.user.id, milestone.id as milestone_table_id, milestone.title, milestone.info, milestone.reward_desc, milestone.reward_lauriers from moodyblues.user INNER JOIN user_milestone ON moodyblues.user.id=user_milestone.user_id INNER JOIN milestone ON user_milestone.milestone_id=milestone.id WHERE moodyblues.user.discord_id = $1;"

        result = await db_pool.fetch(query, user_id)

        raw_user_milestones = [dict(row) for row in result]

        user_milestones = {}
        for user_milestone_dict in raw_user_milestones:
            user_milestones[user_milestone_dict["milestone_table_id"]] = [user_milestone_dict["title"], user_milestone_dict["info"], user_milestone_dict["reward_desc"], user_milestone_dict["reward_lauriers"]]
        
    await db_pool.release(connection)
    return user_milestones


async def milestone_success(db_pool, load):
    connection = await db_pool.acquire()
    async with connection.transaction():
            query = "INSERT INTO milestones.user_milestone(user_id, milestone_id, completed, date) values ((SELECT id from moodyblues.user WHERE discord_id=$1), $2, $3, $4);"
            await db_pool.executemany(query, [cargo for cargo in load])
    await db_pool.release(connection)


async def reward_user(db_pool, load):
    connection = await db_pool.acquire()
    async with connection.transaction():
        query = "INSERT INTO user_title(user_id, title_id) VALUES ((SELECT id from moodyblues.user where discord_id = $1), (SELECT title_id from milestone_title WHERE milestone_id = $2));"
        await db_pool.executemany(query, [cargo for cargo in load])
    await db_pool.release(connection)
     

async def check_milestone(bot, db_pool, user_id, table_info_message, fart_count, message):
    milestones_dict = await fetch_milestone(db_pool, table_info_message)
    user_milestones = await fetch_user_milestone(db_pool, user_id)
    user_milestones_not_completed = {}

    for key,value in milestones_dict.items():
        if key in user_milestones:
            continue
        else:
            user_milestones_not_completed[key] = value
            
    if user_milestones_not_completed :
        await is_milestone_completed(bot, db_pool, user_milestones_not_completed, user_id, fart_count, message)



async def is_milestone_completed(bot, db_pool, milestones_dict, user_id, count, message):
    milestone_success_load=[]
    title_load = []
    
    for milestone_id, values in milestones_dict.items():
        requirement = get_requirement(values)

        if count >= requirement :
            date = datetime.utcnow().replace(tzinfo=pytz.utc)
            milestone_cargo = (user_id, milestone_id, True, date)
            milestone_success_load.append(milestone_cargo)

            if values[2]:
                title_cargo = (user_id, milestone_id)
                title_load.append(title_cargo)
            
            await milestone_announcement(bot, values, user_id, count, message)

    await milestone_success(db_pool, milestone_success_load)
    await reward_user(db_pool, title_load)


async def milestone_announcement(bot, values, user_id, count, message):
    title = values[0]
    embed = discord.Embed(title="‎‎‎‎", color=embed_guidelines["milestone_color"])
    user = await bot.fetch_user(user_id)
    embed.add_field(name = title, value = f"*{values[1]}*", inline=False)

    if values[2]:
        recompense_value = f"**{values[2]}**" 
        embed.add_field(name=" ", value=recompense_value)
    
    path_to_token = f"./features/medias/milestones/lauriers/{values[3]}.png"
    
    token_image = discord.File(path_to_token, filename="lauriers.png")
    embed.set_thumbnail(url="attachment://lauriers.png")


    time = common.get_time()
    embed.set_footer(text=f"{time} - Réalisé par {user.name}", icon_url=user.avatar)
    
    
    await message.channel.send(file=token_image , embed=embed)
    token_image.close()


def get_requirement(values):
    requirement = re.findall(r'\d+', values[1])
    if len(requirement) > 1:
        full_number = ''.join(map(str, requirement))

    else:
        full_number = requirement[0]
    full_number = int(full_number)

    return full_number



async def fetch_all_milestone(db_pool, user_id):
    connection = await db_pool.acquire()
    async with connection.transaction():
        query = "select milestone_categories.name, milestone.title, milestone.info, milestone.reward_lauriers, milestone.reward_desc  from milestone inner join milestone_category ON milestone.id=milestone_id INNER JOIN milestone_categories on milestone_category.category_id=milestone_categories.id;"
        fetcher_all_milestone= await db_pool.fetch(query)
        all_milestones_raw_dict = [dict(row) for row in fetcher_all_milestone]

        query2 = "select milestone.title, user_milestone.date from milestone INNER JOIN user_milestone ON user_milestone.milestone_id=milestone.id INNER JOIN moodyblues.user ON user_milestone.user_id=moodyblues.user.id WHERE moodyblues.user.discord_id = $1;"
        fetcher_user_milestone = await db_pool.fetch(query2, user_id)
        user_milestones_raw_dict= [dict(row) for row in fetcher_user_milestone]
        user_milestones_clean_dict = {}
        for user_milestone in user_milestones_raw_dict:
            user_milestones_clean_dict[user_milestone["title"]] = user_milestone["date"]
        

        milestone_categories = []
        milestone_category = {}
        for milestone_dict in all_milestones_raw_dict:
            
            category = milestone_dict["name"]
            title = milestone_dict["title"]

            if title in user_milestones_clean_dict:
                date_completed = user_milestones_clean_dict[title]
                milestone_unique_data = [milestone_dict["title"], milestone_dict["info"], milestone_dict["reward_desc"], milestone_dict["reward_lauriers"], date_completed]

            else:
                milestone_unique_data = [milestone_dict["title"], milestone_dict["info"], milestone_dict["reward_desc"], milestone_dict["reward_lauriers"], None]

            if category in milestone_category:
                milestone_list = milestone_category[category]
                milestone_list.append(milestone_unique_data)

            else:
                if milestone_category:
                    milestone_categories.append(milestone_category)
                    milestone_category = {}

                milestone_category[category] = [milestone_unique_data]
            
        milestone_categories.append(milestone_category)
        
                
    await db_pool.release(connection)
    return milestone_categories
    