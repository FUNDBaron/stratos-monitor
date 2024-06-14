
# Specify waiting time interval after receiving statuses from servers(seconds)
time_long_pause = 600

# Specify waiting time after sending a command to the server(seconds)
# If your nodes stores a large volume of files, then set the parameter to ~50-60 sec or more
time_short_pause = 60  

#Specify the ssh connection port for server
port = 22

#Specify the path to the file script status.py
path_to_status_script = 'status.py'

URL = 'https://api.telegram.org/bot'

#Specify the telegram bot token from Father bot
TOKEN = ''

#Specify the your chat_id from telegram private chat or channel
CHAT_ID = ''


### Specify a list with data for the number of servers you will access, delete the rest
### Specify logins and passwords(or specify the path to the files with the ssh-keys) of your servers
### If you use 'sshkey' then leave the 'password' field empty string as '', but if use password then leave the 'sshkey' field empty string as ''
### If you run the script 'scan_servers' on a local machine where the resource nodes are located, then specify 'localhost' as True only for this server
### Attention: to create a valid RSA format private ssh-key supported by Paramiko
### In Puttygen click on Conversions then Export OpenSSH Key (for private key)
### For example:
# servers = [
# {
#       'name': 'stratos1'
#       'ip': 'xx.xx.xxx.xxx',
#       'login' : 'YOUR_LOGIN_HERE',
#       "password": 'YOUR_PASS_HERE',
#       'sshkey': '',
#       "localhost": True
# },
# {
#       'name': 'stratos2'
#       'ip': 'xx.xx.xxx.xxx',
#       'login' : 'YOUR_LOGIN_HERE',
#       'password': '',
#       'sshkey': 'ssh-keys/id_rsa',
#       'localhost': False
# },
# {
#       'name': 'stratos3'
#       'ip': 'xx.xx.xxx.xxx',
#       'login' : 'YOUR_LOGIN_HERE',
#       'password': 'YOUR_PASS_HERE',
#       'sshkey': '',
#       'localhost': False
# }]
###
servers = [
{
       'name': 'stratos1',
       'ip': '',
       'login' : '',
       'password': '',
       'sshkey': '',
       'localhost': False
},
{
       'name': 'stratos2',
       'ip': '',
       'login' : '',
       'password': '',
       'sshkey': '',
       'localhost': False
},
{
       'name': 'stratos3',
       'ip': '',
       'login' : '',
       'password': '',
       'sshkey': '',
       'localhost': False
},
{
       'name': 'stratos4',
       "ip": '',
       'login' : '',
       'password': '',
       'sshkey': '',
       'localhost': False
},
{
       'name': 'stratos5',
       'ip': '',
       'login' : '',
       'password': '',
       'sshkey': '',
       'localhost': False
},
{
       'name': 'stratos6',
       "ip": '',
       'login' : '',
       'password': '',
       'sshkey': '',
       'localhost': False
}]

