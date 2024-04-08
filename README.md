# TFT Queue Tracker (Discord Bot)

## Installation

Start by following Discord's own instructions for setting up a bot: https://discordpy.readthedocs.io/en/stable/discord.html

Once you have the bot setup, copy the token provided and find the line at the top of bot.py where it says BOT_TOKEN = MY_TOKEN. Replace MY_TOKEN with your own token. 

Make sure your league client is open, as the LCU API (League Client Update API) requires an open client to function.

First run api.py, which will generate friends_list.json. Then run bot.py. Once both programs are running you can start using the bot!

## Usage

Once the bot has been installed onto one of your discord servers, you can DM it the following commands.

**!list**: This command lists all the active players on your friends list. I recommend you always do this first, because the league client stores old versions of people’s names, even after a name change. For example, “Lab039erinkuma” is still just “erinkuma” on my league client, and the bot won’t be able to track them if you input the new name.

**!add “name”**: Adds the person you chose on your tracking list. If the person’s name has spaces, you have to put their name in quotes, like !add “Lab 013 Vanilla”. Note that you can only add people who are currently online.

**!remove “name”**: Removes a player from your tracking list, follows the same rules as above.

**!track**: Tracks all the people you added to your tracking list, and notifies you when they get in queue.

**!list track**: Shows you all the people who are in your tracking list and their current game status. 

*Note: The way that the league client displays status’s is as follows:
Chat: Online 
Away: Away
dnd: In queue or in game

Finally, this program only works for people who are playing on pc’s unfortunately. When someone gets in game on mobile, it still shows them as being just online, so the program isn’t able to track them.
