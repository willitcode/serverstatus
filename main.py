#!/bin/bash/python3

import configparser
from os import path, system
import asyncio
from discord.ext import commands
import discord

# I'm well aware this is a non-standard thing to call the bot instance. It's the way I like to do it.
client = commands.Bot(command_prefix = '%', help_command=None)

# Read config
config = configparser.ConfigParser()
if path.isfile('config.ini'):
    config.read('config.ini')
else:
    # If the config file doesn't exist, create it
    config['config'] = {'token': '',
            'status': "echo 'R'; while true; do echo 'E'; done",
            'success_message': '{address} appears to have come back up. Phew!',
            'error_message': '{address} appears to have gone down!'}
    config['servers'] = {}
    config['channels'] = {}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    config.read('config.ini')

# This keeps track of the last response from each server so that we don't send a message EVERY SINGLE MINUTE while the server is down and so that we can send a message when the server comes back up
last_response={}
for i, x in config['servers'].items():
    # Set to true on startup. Yes, it will send a message if a server is down every time the script is restarted. That's intended behavior, I think it's actually pretty useful.
    last_response[x]=True

async def send_message(server_address, is_success):
    """Send a message to the channel(s) specified in config.ini using the format specified in config.ini if a server goes down or come back up after being down"""
    # Yes, the variable i is unused, but otherwise we'd have to unpack the tuple on the next line, which would be even messier than this. Maybe we should just change how we use the config, but for right now it's staying how it is. This applies to all the other for statements like this in here as well.
    for i, x in config['channels'].items():
        channel = client.get_channel(int(x))
        if is_success == True:
            await channel.send(config['config']['success_message'].format(address=server_address))
        else:
            await channel.send(config['config']['error_message'].format(address=server_address))

async def ping_servers():
    """Ping the servers specified in config.ini and call send_message if a server goes down or comes back up after being down"""
    # For every server defined in config.ini
    for i, x in config['servers'].items():
        # Ping the server
        response = system('ping -c 1 ' + x + ' >/dev/null')
        if response == 0:
            if last_response[x] == False:
                # If it is up and the last response was that it was down, send a message that it's back up
                await send_message(x, True)
            # Set that the last response was up
            last_response[x] = True
        else:
            if last_response[x] == True:
                # If it is down and the last response was that it was up, send a message that it's down
                await send_message(x, False)
            # Set that the last response was down
            last_response[x] = False


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.online, activity=discord.Game(config['config']['status']))
    # Periodically check the servers
    while True:
        await ping_servers()
        # Only check the servers every minute so we don't get our asses rate limited to hell and back
        await asyncio.sleep(60)

@client.command(pass_context = True)
async def help(ctx):
    embed = discord.Embed(title='Help',
            color=discord.Color(0x000000))
    embed.add_field(name='%ping', value='Check if the bot is online/working. Also outputs the bot\'s latency.')
    embed.add_field(name='%checknow', value='Check if the servers are online *now*. (Rather than waiting for the bot to automatically check them, which it does every 60 seconds.)')
    await ctx.send(embed=embed)

@client.command(pass_context = True)
async def checknow(ctx):
    await ping_servers()

@client.command(pass_context = True)
async def ping(ctx):
    await ctx.send('Pong! Latency: {0}ms'.format(round(client.latency * 1000, 1)))

client.run(config['config']['token'])
