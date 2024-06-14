# Stratos monitoring and notifications nodes
This is a tool used to connect to the servers and obtain information about the status info of running Stratos nodes and send status/storage/rewards data to the monitoring console and telegram chat notifications.

## Install
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
## Pre-Configure
Here you install the client, the current client is Telegram. You will need to provide the ID of the channel you want to send messages to and the Telegram bot API key accordingly.

### Create a Telegram Bot and get a Bot Token:
[How to get Telegram API key](https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token)

### Get Chat ID for a Private Chat:

1. Search and open our new Telegram bot
2. Click `\start` or send any a message
3. Create new your **private** chat, for example `sds-monitor`
4. Add our Telegram bot into a **private** chat and make him an **administrator**
5. Send a message to your the **private** chat, for example: `hello`
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

## Configure files

To run the tool stratos-monitor yourself:
### Location files:
1. Clone the repository:
```
git clone https://github.com/FUNDBaron/stratos-monitor
```
2. Change directory on:
```
cd stratos-monitor
```
3. Place the `status.py` script on each of the servers where Stratos node resource running, for example: in the user `$HOME` directory
4. On each server in the `status.py` file in the `node_dirs` list change the absolute paths where your resource nodes are located
5. Place the `scan_servers.py` and `connect.py` scripts on the server from which the script will connect to the Stratos servers

### Configure the `сonnect.py` file:
Parameters:
- `time_long_pause` - the waiting time interval after which you want to check statuses nodes on each server
* `time_short_pause` - timeout interval for the `status.py` script to complete execution (the more data your nodes store, the longer the interval should be specified)
+ `path_to_status_script` - path to the `status.py` file starting from the home directory of the logged in user(default: $HOME directory)
- `TOKEN` - telegram API Token received from the Father_bot when creating your new_bot
* `CHAT_ID` - chat identifier to which notifications about node statuses will be sent

Then specify the list of servers and connection authentication data: `name`,`ip`,`login`,
- `password` or `sshkey` - path to ssh the private key file (specify the path relative to the location of the `connect.py` and `scan_servers.py` files),
* set the value `localhost: True` on one server in the list if you run the script `scan_servers.py` on the server where the Stratos nodes resource is located, otherwise leave  `localhost: False`

## Run
To connect servers and check statuses automatically
 - We will use the `screen` tool:
```
apt-get install screen
```
* Start a session with name `status`:
```
screen -S status
```
+ Go to the directory where the `scan_servers.py` script is located:
- Lets run script:
```
python3 scan_servers.py
```
## Notes
+ To disconnect from **screen**, enter the combination *Ctrl+A, D* on your keyboard (first press *Ctrl+A*, then *D* together)
- To view a list of screen sessions, run the command:
```
screen -ls
```
* To join an existing session again:
```
screen -r status
```
To exit the **screen** session and close it, enter `exit` or press the combination *Ctrl+D*








