import discord
from discord import RawReactionActionEvent, Message
from discord.ext import commands
from discord.utils import get
import json

"""with open('OpenDMs.json') as f:
OpenDMs = json.loads(str(f))"""
f = open("Schedule.json", "r")
Schedules = json.load(f)
OpenDMs = {}

bot = commands.Bot(command_prefix='$')
bot.remove_command('help')

@bot.command()
async def help(ctx):
    await ctx.send('Commands:\naddGame')
    


@bot.command()
@commands.has_role('leadership')
async def addGame(ctx):
    await ctx.message.author.send('Please respond with game information for example `Scrim against Globochem at 9:00 PM EST on Monday`')
    OpenDMs[ctx.message.author.id] = ctx.message.guild
    

@bot.command()
async def stop(ctx):
    if str(ctx.message.author) == "Anonymouse#5776":
        await bot.close()
        with open("Schedule.json", "w") as f:
            json.dump(Schedules, f)
        with open("OpenDMs.json", "w") as f:
            json.dump(OpenDMs, f)


@bot.event
async def on_message(message: Message):
    if message.guild is None and message.author != bot.user:
        for ch in OpenDMs[message.author.id].text_channels:
            if ch.name == "scheduling":
                channel = ch
        schedule = await channel.send(message.content)
        lineup = await channel.send(f"Not Enough Reactions")
        Schedules[str(schedule.id)] = {"Schedule": schedule.id, "Lineup": lineup.id, "Guild_ID": schedule.guild.id, "Channel_ID": schedule.channel.id}
        OpenDMs.pop(message.author.id)
    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload: RawReactionActionEvent):
    await reaction_change(payload)

@bot.event
async def on_raw_reaction_remove(payload: RawReactionActionEvent):
    await reaction_change(payload)

async def reaction_change(payload: RawReactionActionEvent):
    if str(payload.message_id) in Schedules:
        reactionsClean = []
        reactions = await bot.fetch_channel(Schedules[str(payload.message_id)]["Channel_ID"])
        reactions = await reactions.fetch_message(payload.message_id)
        reactions = reactions.reactions
        for reaction in reactions:
            if reaction.emoji.guild_id == Schedules[str(payload.message_id)]['Guild_ID']:
                reactionsClean.append(reaction)
        
        content = "Not enough reactions!"
        if len(reactionsClean) == 5:
            content = "Map 1 - 3 |"
            for react in reactionsClean:
                content += f" {react.emoji.name}"
        elif len(reactionsClean) == 6:
            content = "Map 1 & 2 |"
            for react in reactionsClean[:5]:
                content += f" {react.emoji.name}"

            content += "\nMap 3 |"
            for react in reactionsClean[:4]:
                content += f" {react.emoji.name}"
            content += f" {reactionsClean[5].emoji.name}"
        elif len(reactionsClean) == 7:
            content = "Map 1 |"
            for react in reactionsClean[:5]:
                content += f" {react.emoji.name}"

            content += "\nMap 2 |"
            for react in reactionsClean[:4]:
                content += f" {react.emoji.name}"
            content += f" {reactionsClean[5].emoji.name}"

            content += "\nMap 3 |"
            for react in reactionsClean[:4]:
                content += f" {react.emoji.name}"
            content += f" {reactionsClean[6].emoji.name}"
        elif len(reactionsClean) == 8:
            content = "Map 1 |"
            for react in reactionsClean[:5]:
                content += f" {react.emoji.name}"

            content += "\nMap 2 |"
            for react in reactionsClean[:4]:
                content += f" {react.emoji.name}"
            content += f" {reactionsClean[5].emoji.name}"
        
            content += "\nMap 3 |"
            for react in reactionsClean[:3]:
                content += f" {react.emoji.name}"
            content += f" {reactionsClean[6].emoji.name}"
            content += f" {reactionsClean[7].emoji.name}"

        msg = await bot.fetch_channel(Schedules[str(payload.message_id)]["Channel_ID"])
        msg = await msg.fetch_message(Schedules[str(payload.message_id)]['Lineup'])
        await msg.edit(content=content)

print('Bot Starting')
bot.run(open("token.txt", "r").read())