
async def fetch_user(db_pool, user_id, is_message = False, is_fart = False, is_pdm = False, is_milestone=False):
    
    connection = await db_pool.acquire()
    async with connection.transaction() :
        message_query = "SELECT moodyblues.user.pseudo, count(moodyblues.user_message.id) as total_message from moodyblues.user INNER JOIN moodyblues.user_message ON moodyblues.user.id=moodyblues.user_message.user_id WHERE moodyblues.user.discord_id=$1 GROUP BY moodyblues.user.pseudo;"

        farte_query = "SELECT moodyblues.user.pseudo, count(moodyblues.user_fart.id) as fart_count from moodyblues.user INNER JOIN moodyblues.user_fart  ON moodyblues.user.id=moodyblues.user_fart.user_id WHERE moodyblues.user_fart.is_emitter = 't' AND moodyblues.user.discord_id=$1 GROUP BY moodyblues.user.pseudo;"

        fartr_query = "SELECT moodyblues.user.pseudo, count(moodyblues.user_fart.id) as fart_count from moodyblues.user INNER JOIN moodyblues.user_fart  ON moodyblues.user.id=moodyblues.user_fart.user_id WHERE moodyblues.user_fart.is_emitter = 'f' AND moodyblues.user.discord_id=$1 GROUP BY moodyblues.user.pseudo;"

        pdme_query = "SELECT moodyblues.user.pseudo, count(moodyblues.user_pdm.id) as pdm_count from moodyblues.user INNER JOIN moodyblues.user_pdm  ON moodyblues.user.id=moodyblues.user_pdm.user_id WHERE moodyblues.user_pdm.is_emitter = 't' AND moodyblues.user.discord_id=$1 GROUP BY moodyblues.user.pseudo;"

        pdmr_query = "SELECT moodyblues.user.pseudo, count(moodyblues.user_pdm.id) as pdm_count from moodyblues.user INNER JOIN moodyblues.user_pdm  ON moodyblues.user.id=moodyblues.user_pdm.user_id WHERE moodyblues.user_pdm.is_emitter = 'f' AND moodyblues.user.discord_id=$1 GROUP BY moodyblues.user.pseudo;"


        message_query_result= await db_pool.fetchrow(message_query, user_id)
        if not message_query_result :
            message_count = 0
        else:
            message_count_dict = dict(message_query_result)
            message_count = int(message_count_dict["total_message"])

        farte_query_result= await db_pool.fetchrow(farte_query, user_id)
        if not farte_query_result:
            farte_count = 0
        else:
            farte_count_dict = dict(farte_query_result)
            farte_count = int(farte_count_dict["fart_count"])
        
        fartr_query_result= await db_pool.fetchrow(fartr_query, user_id)
        if not fartr_query_result:
            fartr_count = 0
        else:
            fartr_count_dict = dict(fartr_query_result)
            fartr_count = int(fartr_count_dict["fart_count"])

        pdme_query_result= await db_pool.fetchrow(pdme_query, user_id)
        if not pdme_query_result:
            pdme_count = 0
        else:
            pdme_count_dict = dict(pdme_query_result)
            pdme_count = int(pdme_count_dict["pdm_count"])

        pdmr_query_result= await db_pool.fetchrow(pdmr_query, user_id)
        if not pdmr_query_result:
            pdmr_count = 0
        else:
            pdmr_count_dict = dict(pdmr_query_result)
            pdmr_count = int(pdmr_count_dict["pdm_count"])

    await db_pool.release(connection)
    
    if is_milestone :
        return message_count, farte_count, fartr_count, pdme_count, pdmr_count

    elif is_message : 
        return message_count

    elif is_fart:
        return farte_count, fartr_count
    
    elif is_pdm:
        return pdme_count, pdmr_count
    else:
        return message_count, farte_count, pdme_count


async def fetch_laurier(db_pool, user_id):
    connection = await db_pool.acquire()
    async with connection.transaction():
        query_user_lauriers = "select moodyblues.user.pseudo, sum(reward_lauriers) as lauriers from moodyblues.user inner join user_milestone on user_id=moodyblues.user.id inner join milestone on milestone_id=milestone.id WHERE moodyblues.user.discord_id=$1  GROUP BY moodyblues.user.pseudo;"

        query_total_lauriers = "SELECT SUM(reward_lauriers) from milestone;"

        fetcher_user_lauriers = await db_pool.fetchrow(query_user_lauriers, user_id)
        if not fetcher_user_lauriers:
            user_lauriers = 0
        else:
            user_lauriers_dict=dict(fetcher_user_lauriers)
            user_lauriers = int(user_lauriers_dict["lauriers"])
        
        fetcher_total_lauriers = await db_pool.fetchrow(query_total_lauriers)
        total_lauriers_dict=dict(fetcher_total_lauriers)
        total_lauriers=int(total_lauriers_dict["sum"])


    await db_pool.release(connection)
    return user_lauriers, total_lauriers


async def fetch_active_title(db_pool, user_id):
    connection = await db_pool.acquire()
    async with connection.transaction():
        query_title = "Select title from user_title INNER JOIN moodyblues.user ON moodyblues.user.id=user_title.user_id INNER JOIN title ON user_title.title_id=title.id  where active=True AND moodyblues.user.discord_id=$1;"

        fetcher_title = await db_pool.fetchrow(query_title, user_id)

        if not fetcher_title:
            title = None

        else : 
            title_dict = dict(fetcher_title)
            title = title_dict["title"]

    await db_pool.release(connection)
    return title

async def fetch_titles(db_pool, user_id):
    connection = await db_pool.acquire()
    async with connection.transaction():
        query = "select moodyblues.user.id as user_id, title.id as title_id, title from title INNER JOIN user_title ON title_id=title.id INNER JOIN moodyblues.user ON moodyblues.user.id=user_title.user_id WHERE moodyblues.user.discord_id=$1;"

        fetcher_title = await db_pool.fetch(query, user_id)
    
        title_dict_clean = {}

        if fetcher_title:   
            raw_dict = [dict(row) for row in fetcher_title]
            no_title = False

            for title_dict in raw_dict:
                title_dict_clean[title_dict["title"]] = [title_dict["user_id"], title_dict["title_id"]]
        else:
            no_title = True
            
    await db_pool.release(connection)

    return title_dict_clean, no_title
