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

    # Sends the user a general list of all online friends and their status's
    if member != 'track':
        with open('friends_list.json', 'r') as json_file:
            friends = json.load(json_file)

        for friend in friends:
            if friends[friend] == 'chat' or friends[friend] == 'dnd' or friends[friend] == 'away':
                temp = 'Friend: ' + friend + '\t\tStatus: ' + friends[friend]
                friend_list += temp + '\n'

    # Sends the user a list of their tracked list members and their status's
    else:
        for friend in track_list:
            temp = 'Friend: ' + friend + '\t\tStatus: ' + track_list[friend][0]
            friend_list += temp + '\n'

    await channel.send(friend_list)


@bot.command(name='track', help='Tracks members on your track list and notifies you when they are in queue')
async def track_queue(ctx):
    channel = ctx.channel

    # Create a toggle variable in json to turn the function on and off
    toggle = {'Status': True}
    with open('toggle.json', 'w') as toggle_file:
        json.dump(toggle, toggle_file)
    toggle_file.close()

    # Function continues to run while the toggle variable is true
    while toggle['Status'] == True:

        # Create a dictionary with data from friends_list json
        with open('friends_list.json', 'r') as json_file:
            friends = json.load(json_file)
        json_file.close()

        send = False
        tracked_friends = ''

        # Runs through all entries in friends list, and use it to update tracklist
        for friend in track_list:
            if len(track_list[friend]) < 2:
                try:
                    track_list[friend].append(friends[friend])
                except KeyError as e:
                    pass
            else:
                prev = track_list[friend][0]
                curr = track_list[friend][1]

                # Shows that the tracked player has gotten into queue and notifies the user
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

        # Update toggle variable to decide whether the function keeps running or not
        with open('toggle.json', 'r') as toggle_file:
            toggle = json.load(toggle_file)
        toggle_file.close()
        await asyncio.sleep(5)


@bot.command(name='queue', help='turns off the tracker when you are in game and turns it on when you are not')
async def in_queue(ctx):
    channel = ctx.channel
    me_track = []

    while True:

        # Uses a separate json file to track the user's status
        with open('me.json', 'r') as json_file:
            me = json.load(json_file)

        if len(me_track) < 2:
            me_track.append(me['me'])
        else:
            prev = me_track[0]
            curr = me_track[1]

            # Changes the toggle status so that the track function turns off
            if curr == 'dnd':
                with open('toggle.json', 'w') as toggle_file:
                    json.dump({'Status': False}, toggle_file)
                toggle_file.close()

            # Turns the track function back on
            elif prev == 'dnd' and curr == 'chat':
                await ctx.invoke(bot.get_command('track'))

            # Update me.json
            me_track.append(me['me'])
            me_track.pop(0)
        await asyncio.sleep(5)

@bot.command(name='check', help='Chceks if the track function is currently on')
async def check_track(ctx):
    channel = ctx.channel
    with open('toggle.json', 'r') as toggle_file:
        toggle = json.load(toggle_file)['Status']
    toggle_file.close()

    if toggle:
        await channel.send('Track function is currently on')
    else:
        await channel.send('Track function is currently off')


@bot.command(name='toggle', help='Toggles the track function')
async def toggle_track(ctx):
    channel = ctx.channel

    # Check the status of track function
    with open('toggle.json', 'r') as toggle_file:
        toggle = json.load(toggle_file)['Status']
    toggle_file.close()

    # Turn it off if it's on, and vice versa
    if toggle:
        with open('toggle.json', 'w') as toggle_file:
            json.dump({'Status': False}, toggle_file)
        toggle_file.close()
        await channel.send('Track function has been turned off')
    else:
        await channel.send('Track function has been turned on')
        await ctx.invoke(bot.get_command('track'))

bot.run(BOT_TOKEN)

