

async def user_fetch(message, users_dict):
    """Generate tuple of data of discord user to insert into database.

    Args:
        message (discord.message): from discord.py API
        user_checklist (dict): the list of the already fetched user

    Returns:
        string if sucessful or None if already in dict 
    """

    # Get user intels
    user_discord_id = message.author.id
    pseudo = message.author.name
    user_created_at = message.author.created_at
    try:
        user_joined_at = message.author.joined_at
    except:
        user_joined_at = message.author.created_at

    # Check if user already fetched from previous messages
    if user_discord_id not in users_dict:
        users_dict[user_discord_id] = " "
        user_crate = (user_discord_id, pseudo, user_created_at, user_joined_at)
        return user_crate
    else:
        return None

async def user_loader(db_pool, user_load):
    """Insert user data into database

    Args:
        db_pool (postgresql pool)
        user_load (tuple): user's info
    """
    # Loads into database
    connection = await db_pool.acquire()

    async with connection.transaction():

        # User's crate into db
        query = "INSERT INTO moodyblues.user (discord_id, pseudo, created_at, joined_at) VALUES ($1, $2, $3, $4);"
        if isinstance(user_load, tuple):
            await db_pool.execute(query, *user_load)
        elif isinstance(user_load, list):
            await db_pool.executemany(query, (crate for crate in user_load))

    await db_pool.release(connection)
    


async def message_fetch(message, chunk_size=0):
    """Generate the tuple containing message data to insert into database

    Args:
        message (discord.Message): discord.py API
        chunk_size (integer): size limit of list to send into database 

    Returns:
        chunk_size concatenated by one, message_crate, user_message_aload_crate, channel_message_aload_crate
    """
    message_discord_id = message.id
    message_content = message.clean_content
    message_created_at = message.created_at

    message_user_id = message.author.id

    message_channel_id = message.channel.id

    message_crate = (message_discord_id, message_content, message_created_at)
    user_message_aload_crate = (message_discord_id, message_created_at, message_user_id)
    channel_message_aload_crate = (message_discord_id, message_created_at, message_channel_id)

    chunk_size +=1  

    return chunk_size, message_crate, user_message_aload_crate, channel_message_aload_crate

async def message_dict(db_pool):
    """Create dict of all discord message's id already in database

    Args:
        db_pool (postgresql.pool)
        message (discord.message)

    Returns:
        dict: all message id in database
    """
    connection = await db_pool.acquire()
    async with connection.transaction():
        query="SELECT discord_id from moodyblues.discord_message"
        result = await db_pool.fetch(query)

        raw_messages = [dict(row) for row in result]
        
        messages = {}
        for milestone_message_dict in raw_messages:
            messages[milestone_message_dict["discord_id"]] = ""
            
    await db_pool.release(connection)
    return messages


async def message_loader(db_pool, message_load):
    """Load the message's data into database

    Args:
        db_pool: ascynpg pool
        message_load : list of tuple of message info
    
    Returns : the message_load empty for further iteration
    """
    # Loads into database
    connection = await db_pool.acquire()

    async with connection.transaction():
        # User's crate into db
        query = "INSERT INTO moodyblues.discord_message (discord_id, content, created_at) VALUES ($1, $2, $3);"
        if isinstance(message_load, tuple):
            await db_pool.execute(query, *message_load)
        elif isinstance(message_load, list):    
            await db_pool.executemany(query, (crate for crate in message_load))

    await db_pool.release(connection)

    message_load=[]

    return message_load



async def channel_fetch(channel, channels_dict):
    """Generate tuple containing channel's data

    Args:
        channel (discord.channel): discord.py API
        channel_cheklist(dict) 

    Returns:
        return channel crate
    """
    channel_discord_id = channel.id 
    channel_category_id = channel.category_id
    channel_name = channel.name
    topic = "Thread"
    nsfw = False
    position = 0
    

    if "Thread" not in str(type(channel)):
        topic = channel.topic
        nsfw = channel.nsfw
        position = channel.position

    if channel_discord_id not in channels_dict:
        channels_dict[channel_discord_id] = " "
        channel_crate = (channel_discord_id, channel_category_id, channel_name, topic, position, nsfw)
        return channel_crate
    else:
        return None

async def channel_loader(db_pool, channel_load):
    """Load channel tuple into database

    Args:
        db_pool (postgresql pool)
        channel_load (tuple): channel info to load into database
    """
    # Loads into database
    connection = await db_pool.acquire()

    async with connection.transaction():

        # User's crate into db
        query = "INSERT INTO moodyblues.discord_channel (discord_id, category_id, channel_name, topic, position, nsfw) VALUES ($1, $2, $3, $4, $5, $6);"

        if isinstance(channel_load, tuple):
            await db_pool.execute(query, *channel_load)
        elif isinstance(channel_load, list):
            await db_pool.executemany(query, (crate for crate in channel_load))

    await db_pool.release(connection)
    

async def user_message_aloader(db_pool, user_message_aload):
    """Fill the association table between user and message

    Args:
        db_pool: asyncpg pool 
        user_message_aload (list of tuples): data for the association
    """
    # Loads into database
    connection = await db_pool.acquire()

    async with connection.transaction():
        # User's crate into db
        query = "INSERT INTO moodyblues.user_message (message_id, user_id) VALUES ((SELECT id from discord_message WHERE discord_id=$1 AND created_at=$2),(SELECT id from moodyblues.user WHERE discord_id=$3));"
        if isinstance(user_message_aload, tuple):
            await db_pool.execute(query, *user_message_aload)
        elif isinstance(user_message_aload, list):
            await db_pool.executemany(query, (crate for crate in user_message_aload), timeout=50000)

    await db_pool.release(connection)

async def channel_message_aloader(db_pool, channel_message_aload):
    """Fill the association table between message and channel

    Args:
        db_pool: asyncpg pool 
        message_channel_aload (list of tuples): data for the association
    """
    # Loads into database
    connection = await db_pool.acquire()

    async with connection.transaction():
        # User's crate into db
        query = "INSERT INTO moodyblues.message_channel (message_id, channel_id) VALUES ((SELECT id from discord_message WHERE discord_id=$1 AND created_at=$2),(SELECT id from moodyblues.discord_channel WHERE discord_id=$3));"
        if isinstance(channel_message_aload, tuple):
            await db_pool.execute(query, *channel_message_aload)
        elif isinstance(channel_message_aload, list):
            await db_pool.executemany(query, (crate for crate in channel_message_aload),  timeout=50000)

    await db_pool.release(connection)

async def fetch_user_message(db_pool, user_id, limit = 1000, random=False):
    """Fetch user discord message in database

    Args:
        db_pool
        user_id (int): user discord id
        limit (int, optional): The quantity of message to retrieve. Defaults to 1000.
        random (boolean, optional) : Select random message, defaults to False : select the last messages sent by user.
    """

    connection = await db_pool.acquire()
    async with connection.transaction():
        query = f"SELECT moodyblues.user.id,  moodyblues.discord_message.content from moodyblues.user INNER JOIN moodyblues.user_message ON moodyblues.user.id = user_message.user_id INNER JOIN moodyblues.discord_message ON moodyblues.discord_message.id = user_message.message_id where moodyblues.user.discord_id = $1 ORDER BY discord_message.created_at DESC limit {limit};"

        result = await db_pool.fetch(query, user_id)
        raw_messages = [dict(row) for row in result]
        
        messages = []
        for message in raw_messages:
            messages.append(message["content"])
        return messages


async def fetch_latest_message(db_pool, channel_id, limit = 100, random=False):
    """Fetch latest discord message in database

    Args:
        db_pool
        limit (int, optional): The quantity of message to retrieve. Defaults to 100.
        random (boolean, optional) : Select random message, defaults to False : select the lastest messages sent by user.
    """

    connection = await db_pool.acquire()
    async with connection.transaction():
        query = f"SELECT moodyblues.user.pseudo, moodyblues.discord_message.content from moodyblues.discord_message INNER JOIN moodyblues.user_message ON discord_message.id = user_message.message_id INNER JOIN moodyblues.user ON user_message.user_id = moodyblues.user.id INNER JOIN moodyblues.message_channel ON message_channel.message_id = discord_message.id INNER JOIN discord_channel ON channel_id=discord_channel.id  WHERE moodyblues.discord_channel.discord_id = $1 ORDER BY discord_message.created_at DESC limit $2 ;"

        result = await db_pool.fetch(query, channel_id, limit)
        raw_messages = [dict(row) for row in result]
        
        messages = []
        for message in raw_messages:
            pseudo = message["pseudo"]
            message_content = message["content"]
            message = f"{pseudo} : {message_content} \n"
            messages.append(message["content"])
        return messages