from datetime import datetime, timedelta

async def scrape_check(db_pool, scrape_key):
    """check into db if article already scraped

    Args:
        db_pool
        scrape_key

    Returns:
        boolean
    """
    connection = await db_pool.acquire()
    async with connection.transaction():
        query = "select 1 from silverscrapes.scrape where scrape_key=$1;"
        result = await db_pool.fetch(query, scrape_key)
        if len(result) > 0:
            exist = True
        else:
            exist = False
    await db_pool.release(connection)
    return exist


async def scrape_loader(db_pool, scrape_load):
    """Load scraped article into database

    Args:
        db_pool
        scrape_load (tuple): Data to load in table scrape
    """
    connection = await db_pool.acquire()

    async with connection.transaction():
        query = "INSERT INTO silverscrapes.scrape(article_date, article_title, article_link, article_desc, website_link, scrape_key, category, to_recap) VALUES($1, $2, $3, $4, $5, $6, $7, $8);"
        await db_pool.execute(query, *scrape_load)
    await db_pool.release(connection) 
    

async def scrape_message_loader(db_pool, mscrape_load):
    """Associate in database scraped article and message sent containing scraped article.

    Args:
        db_pool 
        mscrape_load (tuple): scrape key and message discord id
    """
    connection = await db_pool.acquire()

    async with connection.transaction():
        query = "INSERT INTO silverscrapes.scrape_message(scrape_id, message_id) VALUES((SELECT id from silverscrapes.scrape WHERE scrape_key = $1), (SELECT id from discord_message WHERE discord_id=$2));"
        await db_pool.execute(query, *mscrape_load)
    await db_pool.release(connection)


async def scrape_score(db_pool, message_id):
    """Fetch score of a specific article over the last 24h

    Args:
        db_pool : postgresql pool
        message_id : id of the discord message that had been reacted on
    """

    connection = await db_pool.acquire()

    exist = False
    scrape_id = 0

    async with connection.transaction():
        query = "SELECT message_id, scrape_id from silverscrapes.scrape_message WHERE message_id =(SELECT id from moodyblues.discord_message where discord_id = $1);"
        result = await db_pool.fetchrow(query, message_id)

        if result :
            scrape_id_dict = dict(result)
            scrape_id = int(scrape_id_dict["scrape_id"])
            exist = True
     
    await db_pool.release(connection)
    return exist, scrape_id


async def update_scrape_score(db_pool, scrape_id, add = False, sub = False):
    """Update the score of a specific article over the last 24h

    Args:
        db_pool : postgresql pool
        scrape_id : id of the scrape message that had been reacted on
    """
    connection = await db_pool.acquire()
    async with connection.transaction():
        if add :
            query = "UPDATE silverscrapes.scrape set score = score + 1 where id = $1;"
        if sub :
            query = "UPDATE silverscrapes.scrape set score = score - 1 where id = $1"
        
        await db_pool.execute(query, scrape_id)
    await db_pool.release(connection)


async def fetch_top_news(db_pool):
    """Fetch the news with the highest score in the database

    Args:
        db_pool : postgresql pool
    """
    
    present_day = datetime.now()
    previous_day = present_day - timedelta(days=1)
    
    connection = await db_pool.acquire()
    async with connection.transaction():
        query = f"select id, category, article_title,article_desc from silverscrapes.scrape where article_date > '{previous_day}' AND article_date < '{present_day}' AND to_recap = 't' ORDER BY score  DESC, category DESC LIMIT 5;"


        result = await db_pool.fetch(query)
        raw_all_news_dict = [dict(row) for row in result]
        
        all_news_dict = {}
        for news_dict in raw_all_news_dict:
            category = news_dict["category"]
            article_title = news_dict["article_title"]
            article_desc = news_dict["article_desc"]
            all_news_dict[news_dict["id"]] = f" - {category} - {article_title} : {article_desc}  \n"

    await db_pool.release(connection)
    return all_news_dict