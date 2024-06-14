import paramiko
import time
import socket
import connect
import subprocess
import requests

command_to_server = "python3 {0} -i {1} -n {2} -u {3} -t {4} -c {5}"
result_template = "#######\nServer IP: {0}\nName: {1}\n{2}\n#######"

def get_all_status(        
):
     print(f"The process of receiving STATUSES has started, wait {connect.time_short_pause} seconds...")
     while True:
        for server in connect.servers:
            result = ""
            if server["localhost"] == True:
                try:
                    raw_output = subprocess.check_output(
                        [command_to_server.format(connect.path_to_status_script,
                        server['ip'], 
                        server['name'],
                        connect.URL, 
                        connect.TOKEN,
                        connect.CHAT_ID)],
                        shell = True
                        ) 
                    output = raw_output.decode('utf-8') 
                    result = find_output_mark(output)
                    print(result_template.format(server['ip'], server['name'], result))
                    print(f"Let's check the next server, wait {connect.time_short_pause} more seconds...")
                except subprocess.CalledProcessError as e:
                    errorMsg = ">>>Error while executing:\n"\
                       + command_to_server.format(server['ip'], server['name'])\
                       + "\n>>> Returned with error:\n"\
                       + str(e.output)
                    print("Error: " + errorMsg)
                except FileNotFoundError as e:
                    print("Error: ", e.strerror)
            else:
                try:
                    result = send_command_server(
                        server["ip"],
                        connect.port,
                        server["login"],
                        server["password"],
                        server["sshkey"],
                        command_to_server.format(connect.path_to_status_script, server['ip'], server['name'], connect.URL, connect.TOKEN, connect.CHAT_ID),
                        connect.time_short_pause
                    )
                    if "not found" in result:
                        sent_msg_to_tg_channel(result_template.format(server['ip'], server['name'], f"\U000026A0 {result}"))
                    print(result_template.format(server['ip'], server['name'], result))
                    print(f"Let's check the next server, wait {connect.time_short_pause} more seconds...")
                except Exception as e:
                    sent_msg_to_tg_channel(result_template.format(server['ip'], server['name'], f"\U000026A0 Error: *{str(e)}*"))
                    print(f"\nAn error occurred while recieve answer server: {e}")
                    break        
        print("The STATUSES checking process is completed!\n")
        print(f"The next statuses check will begin in {connect.time_long_pause/60} minutes...")
        time.sleep(connect.time_long_pause)
                
def send_command_server(
    ip,
    port,
    username,
    password,
    ssh_key,
    command,
    short_pause,
    max_bytes=5000
):  
    cl = paramiko.SSHClient()
    cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if password == "" and ssh_key != "":  
        pkey = paramiko.RSAKey.from_private_key_file(ssh_key)
        cl.connect(hostname=ip, port=port, username=username, pkey=pkey, look_for_keys=False, allow_agent=False)
    else:
        cl.connect(hostname=ip, port=port, username=username, password=password, look_for_keys=False, allow_agent=False)
    with cl.invoke_shell() as ssh:
        ssh.send(f"{command}\n") 
        time.sleep(short_pause)
        output = ""
        try:
            output = ssh.recv(max_bytes).decode("utf-8")
            output = find_output_mark(output)
        except socket.timeout as e:
            print(f"Error timeout: " + {e})
            cl.close()
    cl.close()
    return output

def find_output_mark(
    output 
):
    start = output.find(">>>>>") + 5
    end = output.rfind(">>>>>")
    if start and end != -1:
        output = output[start:end]
    else:
        output = "Error: Mark >>>>> not found, *time short pause* is too short"
    return output

def sent_msg_to_tg_channel(
    msg
):
    params = {'chat_id': connect.CHAT_ID,'text': msg, 'parse_mode': 'Markdown'}
    response = requests.get(connect.URL + connect.TOKEN + '/sendMessage', params=params)

get_all_status()
