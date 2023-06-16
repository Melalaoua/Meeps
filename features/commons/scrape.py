import json
import sys, os

from bs4 import BeautifulSoup
import hashlib
import discord
import favicon
from Meeps import cu, embed_guidelines
from datetime import datetime
from parsel import Selector

import asyncio

from features.commons import scrape_sql


async def scrape_handler(web_client, db_pool, browser, scrape_name, data, guild, cat_color, cat_name):
    """Determine which type of scraping it require between HTML (beautifulsoup) and javascript (playwright), send scraped data in discord channel

    Args:
        web_client : the web_client for html request
        db_pool : postgresql pool object 
        browser: browser playwright object 
        scrape_name (str): name of the scraped website
        data : info used for scraping in webscrapping_log.json
        guild : discord guild object

    Returns:
        _type_: return updated data doc
    """

    scraped = False

    text_channel, scrape_data = data
    text_channel_id = text_channel[1]
    channel = guild.get_channel_or_thread(text_channel_id)
    if not channel:
        return
    
    if scrape_data["javascript"]:
        page = await browser.new_page()
        try:   
            scraped, article_embed, new_scrape_data, scrape_name, scrape_key = await scrape_javascript(db_pool, page, scrape_data, scrape_name,  cat_color, cat_name)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            await channel.send(f'**`ERROR - {scrape_name} :`** {type(e).__name__} - {e} - {exc_type} - {fname} - {exc_tb.tb_lineno}')  
            await page.close()
        await page.close()

    else:
        try:
            scraped, article_embed, new_scrape_data, scrape_name, scrape_key = await get_latest_news(web_client, db_pool, scrape_data, scrape_name, cat_color, cat_name)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            await channel.send(f'**`ERROR - {scrape_name} :`** {type(e).__name__} - {e} - {exc_type} - {fname} - {exc_tb.tb_lineno}')  
    
    if scraped:
                message = await channel.send(embed=article_embed)
                await message.add_reaction('👍')
                await message.add_reaction('👎')
                data = (text_channel,new_scrape_data)
                await asyncio.sleep(0.5)
                mscrape_load = (scrape_key, message.id)
                await scrape_sql.scrape_message_loader(db_pool, mscrape_load)

                
    return data
    

def fetch_scraping_list(category):
    """Fetch data in webscrapping_log.json file and retrieve data as doc.

    Args:
        category (str): Category to get in doc

    Returns:
        dict: data from doc. 
    """

    path_logs = "./features/ressources/webscrapping_log.json"
    f = open(path_logs)
    data = json.load(f)

    scraping_list = {}

    for categories in data["categories"]:
        for categorie_n, categorie_d in categories.items():
            if categorie_n == category:
                for subcat_name, subcat_data in categorie_d["subcategories"].items(): 
                    if subcat_data["channel"] :
                        text_channel = ("channel", subcat_data["channel"])

                    if subcat_data["thread"] :
                        text_channel = ("thread", subcat_data["thread"])
                    
                    for website_n, website_data in subcat_data["websites"].items():
                        scraping_list [website_n] = (text_channel, website_data)
    
    return scraping_list



async def get_latest_news(web_client, db_pool, scrape_data, scrape_name, cat_color, cat_name):
    """Scrape website using html scraper beautifulSoup
    Args:
        web_client, db_pool, scrape_data, scrape_name
    """

    previous_key = scrape_data["scraping_key"]
    scraping_url = scrape_data["scraping_url"]
    base_url = scrape_data["url"]

    async with web_client.get(scraping_url) as resp:
        body = await resp.text()
        soup = BeautifulSoup(body, "html.parser")

        latest_article = soup.find(*scrape_data["latest_article"])
        title = latest_article.find(*scrape_data["title"]).text
        title = ' '.join(title.split())
        
        if scrape_data["image_url"]:
            image_url = latest_article.find(*scrape_data["image_url"])[scrape_data["image_src"]]
            if "pcgamer" in scrape_name:
                image_url = image_url.split(" ")[0]
            if "science-vids" in scrape_name:
                image_url = f"{base_url}{image_url}"
            if "techmeme" in scrape_name:
                image_url = f"{base_url}{image_url}"
            if scrape_data["image_not_full"]:
                image_url = f"https:{image_url}"

        elif "gameinformer" in scrape_name :
            image_div = latest_article.find("div", {"class" : "article-image"})
            image_url = image_div[scrape_data["image_src"]]
            image_url = f"{base_url}{image_url}"

        else:
            image_url = False
        
        if scrape_name == "hacker-news":
            article_path = latest_article.find_all(*scrape_data["article_url"])[1]["href"]
        elif scrape_name == "hacker-news-ask":
            article_path = latest_article.find_all(*scrape_data["article_url"])[1]["href"]
        else:
            article_path = latest_article.find(*scrape_data["article_url"])["href"]
            
        if not scrape_data["full_url"]:   
            article_url = f"{base_url}{article_path}"
        else:
            article_url = article_path    

        if scrape_data["desc"]:
            desc = latest_article.find(*scrape_data['desc']).text
        elif scrape_name == "patent-drop":
            desc = latest_article.find_all("a")[1].text
        else:
            desc = "‎"

        if scrape_data["author"]:
            author = latest_article.find(*scrape_data["author"]).text
         
        elif "gameinformer" in scrape_name:
            author_div = latest_article.find("div", {"class" : "author-details article-author"})
            author = author_div.find("a").text 

        else:
            author = "‎"

        website_name = scrape_data["website"]
        icons = favicon.get(base_url)
        favicon_icon_list = int(scrape_data["favicon_icon_list"])
        favicon_url = icons[favicon_icon_list].url


        # embed_color = scrape_data["color"]
        int_colour = int(cat_color,16)

        update = cu["update"]
        article_date = datetime.now()
        
        title_hash = "".join(title.split(" "))
        title_hash = title_hash[0:10]
        scrape_key = int(hashlib.sha1(title_hash.encode("utf-8")).hexdigest(), 16) % (10 ** 8)

        to_recap = scrape_data["to_recap"]

        exist = await scrape_sql.scrape_check(db_pool, scrape_key)
        if exist :
            embed = False
            return False, embed, scrape_data, scrape_name, scrape_key
        
        if scrape_key != previous_key :
            embed = generate_embed(title, desc, int_colour, image_url, author, website_name, update, favicon_url, article_url)
            scrape_data["scraping_key"] = scrape_key
            scrape_load = (article_date, title, article_url, desc, scraping_url, scrape_key, cat_name, to_recap)
            await scrape_sql.scrape_loader(db_pool, scrape_load)
            return True, embed, scrape_data, scrape_name, scrape_key
        else:
            embed = False
            return False, embed, scrape_data, scrape_name



async def get_repository(web_client, previous_key):
    """Scrape github repository for new trending repository, send to discord afterward.
    Args:
        web_client 
        previous_key 
    """

    scraping_url = "https://github.com/trending"
    base_url = "https://github.com/"

    async with web_client.get(scraping_url) as resp:
        body = await resp.text()
        soup = BeautifulSoup(body, "html.parser")

        latest_article = soup.find("article", {"class" : "Box-row"})
        title = latest_article.find("h2").text
        title = ' '.join(title.split())

        article_path = latest_article.find_all("a")[1]["href"]
        article_url = f"{base_url}{article_path}"

        try:
            desc = latest_article.find("p").text
        except:
            desc = "‎"
            
        author = latest_article.find('span', {"itemprop" : "programmingLanguage"}).text 
        image_url = False

        website_name = base_url
        icons = favicon.get(base_url)
        favicon_icon_list = 0
        favicon_url = icons[favicon_icon_list].url

        embed_color = "0x1F6FEB"
        int_colour = int(embed_color,16)

        update = cu["update"]
        
        scrape_key = int(hashlib.sha1(title.encode("utf-8")).hexdigest(), 16) % (10 ** 8)
        if scrape_key != previous_key:
            embed = generate_embed(title, desc, int_colour, image_url, author, website_name, update, favicon_url, article_url)
            return True, embed, scrape_key
        else:
            embed = False
            return False, embed, scrape_key


async def scrape_javascript(db_pool, page, scrape_data, scrape_name, cat_color, cat_name):
    """Scrape javascript, create new page in browser and retrieve data to send in discord channel. 

    Args:
        db_pool 
        page 
        scrape_data 
        scrape_name 
    """
    previous_key = scrape_data["scraping_key"]
    scraping_url = scrape_data["scraping_url"]
    base_url = scrape_data["url"]

    # navigate to the page
    await page.goto(scraping_url)
    # wait for page to load by checking for presence of a loaded element:
    await page.wait_for_selector(scrape_data["wait_for"])
    # then we can retrieve the page source and parse it
    html = await page.content()
    selector = Selector(html)

    content = selector.xpath(*scrape_data["content"])

    for i, article in enumerate(content):
        if i == 0:
            title = article.xpath(*scrape_data["title"]).get()
        
            if scrape_data["image_url"]:
                image_url = article.xpath(*scrape_data["image_url"]).get()
                if scrape_data["image_not_full"]:
                    image_url = f"https:{image_url}"

            if scrape_data["article_url"]:
                article_path = article.xpath(*scrape_data["article_url"]).get()
                if not scrape_data["full_url"]:
                    article_url = f"{base_url}{article_path}"
                else:
                    article_url = article_path     
            elif scrape_name == "kantrad":
                    article_url = scrape_data["url"]
            else: 
                article_url = False
            
            if scrape_data["desc"]:
                desc = "".join(article.xpath(*scrape_data["desc"]).getall())
            else:
                desc = "‎"


            if scrape_data["author"]:
                author = "".join(article.xpath(*scrape_data["author"]).getall())
            else:
                author = "‎"

            website_name = scrape_data["website"]
            icons = favicon.get(base_url)
            favicon_icon_list = int(scrape_data["favicon_icon_list"])
            favicon_url = icons[favicon_icon_list].url
            # embed_color = scrape_data["color"]
            int_colour = int(cat_color,16)
            update = cu["update"]
            article_date = datetime.now()

            title_hash = "".join(title.split(" "))
            scrape_key = int(hashlib.sha1(title_hash.encode("utf-8")).hexdigest(), 16) % (10 ** 8)

            to_recap = scrape_data["to_recap"]

            exist = await scrape_sql.scrape_check(db_pool, scrape_key)
            if exist :
                embed = False
                return False, embed, scrape_data, scrape_name, scrape_key
            
            if scrape_key != previous_key:
                embed = generate_embed(title, desc, int_colour, image_url, author, website_name, update, favicon_url, article_url)
                scrape_data["scraping_key"] = scrape_key

                scrape_load = (article_date, title, article_url, desc, scraping_url, scrape_key, cat_name, to_recap)
                await scrape_sql.scrape_loader(db_pool, scrape_load)
                
                return True, embed, scrape_data, scrape_name, scrape_key
            
            else:
                embed = False
                return False, embed, scrape_data, scrape_name

      
def generate_embed(title, desc, int_colour, image_url, author, website_name, update, favicon_url, article_url):
    """Generate embed from scraped data to send into discord channel.

    Args:
        title (str): Title of article
        desc (str): Description of article
        int_colour : Color in hex
        image_url (str): url of image
        author (str): Author of article
        website_name (str): name of the website
        update (str): actual update of Meeps
        favicon_url (str): url of website favicon
        article_url (str): url of article 

    Returns:
        object: discord embed
    """
    embed=discord.Embed(title=title, description=desc, color = int_colour)
    if image_url:
        embed.set_image(url=image_url)
    
    if article_url:
        embed.add_field(name=" ", value=f"[Lien vers l'article]({article_url})")

    embed.set_footer(text=f"{author} - {website_name} - {update}", icon_url=favicon_url)

    return embed



# def generate_journal_embed(title, summary):
#     """Take as entry LLM's answer, return discord embed

#     Args:
#         answer (str): LLM answer

#     Returns:
#         _type_: _description_
#     """

#     embed=discord.Embed(title=title, description="L'actualité des dernières 24heures, présentées par Meeps.", color = embed_guidelines["color"])
#     embed.add_field(name="", value=summary)
#     return embed


# async def get_latest_news_notion(web_client, scrape_data, scrape_name):
    
#     previous_key = scrape_data["scraping_key"]
#     url = scrape_data["scraping_url"]
    
#     async with web_client.get(url) as resp:
#         body = await resp.text()
#         soup = BeautifulSoup(body, "html.parser")
  
#         latest_article = soup.find(*scrape_data["latest_article"])
#         data = latest_article.find_all("span")
#         title = data[0].text
#         article_url = data[2].text
#         desc = data[1].text
        

#         icons = favicon.get(url)
#         favicon_url = icons[0].url

#         embed_color = scrape_data["color"]
#         int_colour = int(embed_color,16)

#         scrape_key = int(hashlib.sha1(title.encode("utf-8")).hexdigest(), 16) % (10 ** 8)


#         if scrape_key != previous_key:
#             embed=discord.Embed(title=title, description=desc, color=int_colour)

#             embed.add_field(name=" ", value=f"({article_url})")
#             embed.set_footer(text=f"ML-Quant", icon_url = favicon_url)

#             scrape_data["scraping_key"] = scrape_key
#             return True, embed, scrape_data, scrape_name
#         else:
#             embed = False
#             return False, embed, scrape_data, scrape_name
