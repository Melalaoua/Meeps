
from dotenv import load_dotenv
import openai
import os

import random
import json

load_dotenv()
OPENAI_API_KEY = os.getenv("openAI_API")
openai.api_key = OPENAI_API_KEY

async def prompt_gpt(llm_prompt, chat=False, max_tokens = 250):
    """Ask chatGPT a question if chat is true, make chat completion
    """
    if chat : 
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            max_tokens=max_tokens,
            temperature=0.6,
            messages = llm_prompt)
        return response
    
    else:
        response = openai.Completion.create(
            model="text-davinci-003",
            max_tokens=max_tokens,
            temperature=0.6,
            prompt = llm_prompt)
        return response


async def roast_gpt(user_name, messages):
    """Roast the user using his latest messages sent in the server"""
    prompt = f"En te basant sur les messages de {user_name}, créer une insulte aigrie, humiliante, méchante, rappelle toi d'exclure les mentions d'autres utilisateur. Exclue aussi les prénoms, tu dois te concentrer que sur les sujets des messages : \n {messages} \n roast."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.8,
    )
    
    return response


async def love_gpt(user_name, messages):
    """Love the user using his latest messages sent in the server"""
    prompt = f"En te basant sur les messages de {user_name}, créer un compliment plein d'amour, d'admiration. Rappelle toi d'exclure les mentions d'autres utilisateur. Exclue aussi les prénoms, tu dois te concentrer que sur les sujets des messages : \n {messages} \n "
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.8,
    )
    
    return response

async def generate_prompt_journal(news_list = None, first = True,  persona = None, chat = None, assistant_answer = None):
    """Generate a specific prompt for chatGPT to embody a journalist to make a summary every evening of the news that has been scraped today. If first_prompt is true, it will generate a simple prompt, otherwise if first_prompt is false and the previous prompt is passed, it will return a conversation prompt 

    Args:
        news_list (list): list of all the news chatGPT will make a summary of

    Returns:
        prompt (dict): the prompt
    """

    if first:
        persona_name, persona_carac = fetch_persona()
        user_content = persona_carac[0] + persona_carac[1] + persona_carac[2] + persona_carac[3] + persona_carac[4] + news_list
        chat = [
            {
                "role": "system", "content": "You are a helpful assistant."
            },
            {
                "role" :  "user", "content": user_content
            }
        ]

        return chat, persona_name, persona_carac

    elif not first:
        if chat:
            assistant_answer =  {"role": "assistant", "content": assistant_answer}
            ask_summary = {"role" : "user", "content": persona[5]}

            chat.append(assistant_answer)
            chat.append(ask_summary)

            return chat
            



def fetch_persona():
    """Fetch all persona in persona.json for chatGPT to harbor.

    Returns:
        dict: data from doc. 
    """

    path_logs = "./features/ressources/personas.json"
    f = open(path_logs)
    data = json.load(f)

    personas = {}

    for persona in data["personas"]:
        for persona_name, persona_carac in persona.items():
            personas[persona_name] = [persona_carac["main-prompt"], persona_carac["target"], persona_carac["style"], persona_carac["additional"], persona_carac["ask_title"], persona_carac["ask_summary"]]
    
    persona_name, persona_carac = random_value(personas)
    return persona_name, persona_carac


def random_value(dict_values):
    """Select a random key-value pair in a given dict

    Args : dict
    Return : key, value (separately)
    """

    dict_key, dict_value = random.choice(list(dict_values.items()))
    return dict_key, dict_value

