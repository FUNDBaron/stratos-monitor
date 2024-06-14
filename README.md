# Stratos monitoring and notifications nodes
This is a tool used to connect to the servers and obtain information about the status info of running Stratos nodes and send status/storage/rewards data to the monitoring console and telegram chat notifications.

## Run and Python Dependencies

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

## Configuration

Here you install the client, the current client is Telegram. You will need to provide the ID of the channel you want to send messages to and the Telegram bot API key accordingly.

### Create a Telegram Bot and get a Bot Token:
[How to get Telegram API key](https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token)

### Get Chat ID for a Private Chat:

1. Search and open our new Telegram bot
2. Click Start or send a message
3. Create new your private chat or channel, for example `sds-monitor`
4. Add our Telegram bot into a private chat(channel) and make him an administrator
5. Send a message to your the private chat(channel) for example `hello`
6. Open this URL in a browser: `https://api.telegram.org/bot{our_api_bot_token}/getUpdates`
 - See we need to prefix our token with a wor `bot`
 * Eg: `https://api.telegram.org/bot63xxxxxx71:AAFoxxxxn0hwA-2TVSxxxNf4c/getUpdates`
7. We will see a json like so 
``` 
{
      "update_id": 565837220,
      "channel_post": {
        "message_id": 1235,
        "sender_chat": {
          "id": -100xxxxxxxx45,
          "title": "sds-monitor",
          "type": "channel"
        },
        "chat": {
          "id": -100xxxxxxxx45,
          "title": "sds-monitor",
          "type": "channel"
        },
        "date": 1047188837,
        "text": "hello",
        "has_protected_content": true
}
```
8. Check the value of `.chat.id`, and here is our Chat ID: `-100xxxxxxxx45`
9. Let's try to send a message: `https://api.telegram.org/bot63xxxxxx71:AAFoxxxxn0hwA-2TVSxxxNf4c/sendMessage?chat_id=-100xxxxxxxx45&text=test123`
10. When you set the bot token and chat id correctly, the message `test123` should be arrived on our Telegram bot chat.

## Build

To run the tool stratos-monitor yourself, clone the repository:

```
git clone https://github.com/FUNDBaron/stratos-monitor
```




