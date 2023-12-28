#!/bin/bash/python3

import configparser
from os import path, system
import asyncio
from discord.ext import commands
import discord

# I'm well aware this is a non-standard thing to call the bot instance. It's the way I like to do it.
client = commands.Bot(command_prefix = '%')

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

# This will send a message to the channel(s) specified in config.ini using the format specified in config.ini if a server goes down or come back up after being down
async def send_message(server_address, is_success):
    # Yes, the variable i is unused, but otherwise we'd have to unpack the tuple on the next line, which would be even messier than this. Maybe we should just change how we use the config, but for right now it's staying how it is. This applies to all the other for statements like this in here as well.
    for i, x in config['channels'].items():
        channel = client.get_channel(int(x))
        if is_success == True:
            await channel.send(config['config']['success_message'].format(address=server_address))
        else:
            await channel.send(config['config']['error_message'].format(address=server_address))

# This keeps track of the last response from each server so that we don't send a message EVERY SINGLE MINUTE while the server is down and so that we can send a message when the server comes back up
last_response={}
for i, x in config['servers'].items():
    last_response[x]=True

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.online, activity=discord.Game(config['config']['status']))
    while True:
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
        # Only check the servers every minute so we don't get our asses rate limited to hell and back
        await asyncio.sleep(60)

@client.command(pass_context = True)
async def ping(ctx):
    await ctx.send('Pong!')

client.run(config['config']['token'])
