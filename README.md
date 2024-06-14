# Stratos monitoring and notifications nodes info
Stratos nodes info, monitoring and notifications.
This is a tool used to connect to the servers and obtain information about the status of running Stratos nodes and send status/storage/rewards data to the console and telegram chat.

# Run and Python Dependencies

```
apt-get install python3-pip

pip install paramiko

pip install sockets

pip3 install requests

pip install pexpect

pip install pandas

pip install toml

pip install tabulate

pip install getpass4

pip install argparse

```

# Configuration

Here you install the client, the current client is Telegram. You will need to provide the ID of the channel you want to send messages to and the Telegram bot API key accordingly.

## Create a Telegram Bot and get a Bot Token:
[How to get Telegram API key](https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token)

## Get Chat ID for a Private Chat:

1. Search and open our new Telegram bot
2. Click Start or send a message
3. Open this URL in a browser `https://api.telegram.org/bot{our_bot_token}/getUpdates`
 - See we need to prefix our token with a wor `bot`
 * Eg: `https://api.telegram.org/bot63xxxxxx71:AAFoxxxxn0hwA-2TVSxxxNf4c/getUpdates`

# Build

To run the tool stratos-monitor yourself, clone the repository:

```
git clone https://github.com/FUNDBaron/stratos-monitor

```




