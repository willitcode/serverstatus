# Server Status
A tiny Python script to ICMP ping servers and send a Discord message if they're down.

## Usage
### Outside of Docker
Head over to the [releases](https://github.com/willitcode/serverstatus/releases) and download the file main.py from the latest stable release.

Run main.py (Make sure you're in the same directory with main.py and that it's a directory where you're okay with main.py living semi-permanately):
```shell
python3 main.py
```
It will error out. This is because you need to enter a valid bot token in config.ini. See [configuration](https://github.com/willitcode/serverstatus#configuration) for more information on that.

After configuration, run main.py again to actually start the bot. It's recommended to use some way of autostarting the script and to run it on a machine that will have high uptime, like a server.

### Configuration

First, make sure you've run main.py (or the Docker container) at least once to generate the config file.

Then, edit the configuration file with your text editor of choice. Outside of Docker, it'll be wherever main.py is (provided you ran main.py from the directory that contains main.py). With Docker, it'll be wherever you put it.

Values:
| Value | Description | Required |
| ----- | ----------- | -------- |
| token | The bot token. Information about getting a bot token can be found in [the discord.py documentation](https://discordpy.readthedocs.io/en/latest/discord.html#discord-intro). | Yes |
| status | Discord will display this as what the bot is "playing". It comes set to "echo 'R'; while true; do echo 'E'; done" by default, you can set it to whatever you want. | No |
| error_message | What the bot will send in the specified channel(s) if a server goes down. {address} will be replaced with the address of the server that went down. [See this](https://github.com/willitcode/serverstatus#how-do-i-mention-myself-others-everyone-or-here-in-the-message-the-bot-sends-if-a-server-goes-down-or-comes-back-up) for information about @mentioning people here. | Yes |
| success_message | What the bot will send in the specified channel(s) after a server comes back up. {address} will be replaced with the address of the server that went down. [See this](https://github.com/willitcode/serverstatus#how-do-i-mention-myself-others-everyone-or-here-in-the-message-the-bot-sends-if-a-server-goes-down-or-comes-back-up) for information about @mentioning people here. | Yes |

Next, you need to specify a/some server(s) to monitor. This is a bit weird, so buckle up. Underneath the `[servers]` section, type something like this:
```ini
server1 = <server address here>
```
Technically, "server1" can be whatever you want. It has no effect on what the program does. Continue to add servers until all your servers are added. Just make sure you don't name two servers the same thing.

You also need to specifiy one or more channels to send message(s) to when the server goes down or comes back up. This is very similar to servers. Underneath the `[channels]` section, type something like this:
```ini
channel1 = <channel id here>
```
Again, what "channel1" is set to has no effect on what the program does. Just make sure you don't name two channels the same thing.

How to get a channel's ID:  
1. Make sure you have developer mode on in Discord. If you don't or you're unsure, you can enable it by going to user settings > appearance > developer mode
2. Go to the server that has the channel you want the messages to be sent to in it
3. Right click (or tap and hold) on the channel
4. Click copy ID
5. Paste the ID into config.ini in the appropriate place
6. Repeat steps 2 through 5 until all the channels you'd like messages sent to have been added

## Updating
### Outside of Docker
Delete main.py (DO NOT delete config.ini), download the new main.py from the [releases](https://github.com/willitcode/serverstatus/releases), put it where the old main.py was, and run it again/restart your service. Simple as that.

## Contributing
Just open a pull request! That's what open source is all about. 

If you don't know how to code but you found a bug or have an issue, open an issue.

## FAQ
### How do I @mention myself, others, @everyone, or @here in the message the bot sends if a server goes down or comes back up?
With @everyone and @here, it's easy. Just type @everyone or @here where you want the mention to be.

However, if you want to mention a specific person, it's a bit harder. First, you need to get your user ID:
1. Make sure you have developer mode on in Discord. If you don't or you're unsure, you can enable it by going to user settings > appearance > developer mode
2. Find the user you want to mention somewhere
3. On desktop: right-click the user and click copy ID
3. On mobile: tap on the user to bring up their profile, click the three dots in the top right, and click copy ID.

Then, open the config, and where you want the mention, put:
```ini
<@user ID here>
```
NOTE: The @ is VERY important.
