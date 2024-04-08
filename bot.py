import asyncio
import discord
from discord.ext import commands
import json

BOT_TOKEN = 'YOUR TOKEN HERE'

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
track_list = {}


with open('friends_list.json', 'r') as json_file:
    friends = json.load(json_file)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord')


@bot.event
async def on_shutdown():
    print('Shutting down...')


@bot.command(name='add', help='Adds a player to your tracking list in the format !add Name')
async def add_player(ctx, game_name):
    channel = ctx.channel
    if game_name not in track_list:
        if game_name in friends:
            track_list[game_name] = []
            track_list[game_name].append(friends[game_name])
            await ctx.send(game_name + ' has been added to your tracking list')
        else:
            await channel.send(game_name + ' is not online or not on your friends list')


@bot.command(name='remove', help='Removes a player from your tracking list')
async def delete_player(ctx, game_name):
    channel = ctx.channel
    if game_name not in track_list:
        await ctx.send(game_name + ' is not on your tracking list')
    else:
        del track_list[game_name]
        await channel.send(game_name + ' has been removed from your tracking list')


@bot.command(name='list', help='Lists all online players on your friends list.')
async def list_friends(ctx, member: str = None):
    channel = ctx.channel
    friend_list = ''
    if member != 'track':
        with open('friends_list.json', 'r') as json_file:
            friends = json.load(json_file)

        for friend in friends:
            if friends[friend] == 'chat' or friends[friend] == 'dnd' or friends[friend] == 'away':
                temp = 'Friend: ' + friend + '\t\tStatus: ' + friends[friend]
                friend_list += temp + '\n'
    else:
        for friend in track_list:
            temp = 'Friend: ' + friend + '\t\tStatus: ' + track_list[friend][0]
            friend_list += temp + '\n'

    await channel.send(friend_list)


@bot.command(name='track', help='Tracks members on your track list and notifies you when they are in queue')
async def track_queue(ctx):
    channel = ctx.channel
    user = ctx.author
    while True:
        with open('friends_list.json', 'r') as json_file:
            friends = json.load(json_file)

        send = False
        tracked_friends = ''
        for friend in track_list:
            if len(track_list[friend]) < 2:
                try:
                    track_list[friend].append(friends[friend])
                except KeyError as e:
                    pass
            else:
                prev = track_list[friend][0]
                curr = track_list[friend][1]
                if prev == 'chat' and curr == 'dnd':
                    tracked_friends += friend + ' has just gotten in queue\n'
                    send = True
                try:
                    track_list[friend].append(friends[friend])
                    track_list[friend].pop(0)
                except KeyError:
                    pass
        if send:
            await channel.send(tracked_friends)
        await asyncio.sleep(5)

bot.run(BOT_TOKEN)

