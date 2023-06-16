import discord
from discord.ext import commands

import os
from pathlib import Path

from discord import FFmpegPCMAudio
import random

import pytz
from datetime import datetime

from features.commons import milestone_handler, user_info

ref_sound_pack = "./cogs/iref/ref_sound_pack/"


dict_ref = {
    "skype": "skype.wav",
    "stonks": "STONKS.wav",
    "kebab-kebab": "un-petit-kebab.wav",
    "wasted": "Wasted_GTA.wav",
    "yuki": "yukki_1.wav",
    "apagnan": "Tas_les_cramptesApagnanQUOICOUBEHHH.wav",
    "zbeub": "zbeub_zbeub.wav",
    "macron-macron": "macron_macron.wav",
    "alder": "ALDER.wav",
    "suuuu": "suuuu.wav",
    "bizarre": "Bizarre.wav",
    "cringe": "cringe.wav",
    "OSBLC": "osblc.wav",
    "grigny": "grigny.wav",
    "667" : "667.wav",
    "super" : "Super.wav",
    "greg" : "greg.wav"
}


class ref(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.db_pool = self.bot.db_pool


    def get_ref_sound(self, ref_name):
        path_ref_sound = ref_sound_pack + dict_ref[str(ref_name)]
        return path_ref_sound

    def play_sound_continious(self, voice, ref_name):
        playsound = True

        while True:
            if voice.is_playing():
                continue
            elif playsound == False:
                break
            elif playsound == True:
                if ref_name not in dict_ref:
                     return False
                ref = self.get_ref_sound(ref_name)
                source = FFmpegPCMAudio(ref)
                voice.play(source)
                playsound = False
        return ref


    @commands.command(name="ref")
    async def play_ref(self, ctx, member:discord.Member, ref_name) -> None:
        """Personal soundboard that user in the server can use. Join voice channel of the target to play sound. 

        Args:
            ctx (discord.context)
            member (discord.Member)
            ref_name (str)
        """
        channel = member.voice.channel
        voice = await channel.connect()
        ref = self.play_sound_continious(voice, ref_name)
        await voice.disconnect()

    @commands.command(name="ref-catalog")
    async def ref_catalog(self, ctx) -> None:
        str_output = ""
        for k, v in dict_ref.items():
            str_output += str(k) + "\n"
        await ctx.send(str_output)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ref(bot))
