from datetime import datetime, timedelta
import discord
import json

import random


def string_factory(*args):
    """Take strings as args, return string concatenated

    Returns:
        str : all args concatenated
    """
    data_string=""

    for arg in args:
        data_string = data_string + str(arg)
    
    return data_string

def get_time():
    """Return time utc + 2 

    Returns:
        datetime: "00h00" format
    """
    now = datetime.now()
    now = now + timedelta(hours=2)
    time = now.strftime("%Hh%M") 
    return time

def fetch_commands():
    """Get all commands inside json containing Meeps's commands

    Returns:
        dict: dict containing commands data
    """
    f = open("./features/ressources/commands.json")
    data = json.load(f)

    commands_data = []

    for k1,v1 in data.items():
        for categories in data[k1]:
            for k2, v2 in categories.items():
                for k3, v3 in v2.items():
                    if k3 == "title":
                        category = v3
                    if k3 == "commands":
                        for k4,v4 in v3.items():
                            command_dict = {}
                            command_name = v4["command_name"]
                            command_dict[command_name] = [v4["emoji"], v4["command_desc"], v4["command_usage"], v4["associated_channel"]]
                            
                            commands_data.append(command_dict)

    return commands_data


def rand_number():
    """Generate random number between 20 and 40 used for asyncio.sleep() scraping section.

    Args: 
        
    Returns:
        int: between args
    """
    waiting_time = random.randint(20,40)
    return waiting_time

