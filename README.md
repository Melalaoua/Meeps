# Meeps
My personal discord bot 


This bot combine everything I've learned throughout my years in progamming. I started from here and compounded every discovery, learning made in my studies. 

Meeps act as a sandbox to try new technologies for me and my friends on my server.

The cog folder is divided by multiple functions : 

### Common
- React_role : react_role command to add role to users.
- Book : help command.
- Owner : Commands restricted to server owner.
- Update : Display latest update and patch of the bot.

### iRef
Personal soundboard playing sound in discord.

### llm
OpenAI interaction with GPT
- Roast : roast command
- Recap : recap made every day at 8:30 PM of all the data scraped today by the bot (see folder Ww)

### messages
Message handling, all discord messsage are stored on a personal databse (postgresql).

### Milestones
Success system built in order to track each user metric (message count, game played, ...) and give reward depending on the success.

### User
Display user data
- title_select : milestone can give access to various title
- user : display avatar, other metrics (message count, milestone points, ...)


### ww
Scraping function
- Gaming, Tech, .. : scrape data using beautiful soup and/or playwright to scrape data and send in various discord channels
