import os
import pexpect
import pandas as pd
import toml
from tabulate import tabulate
import getpass
import requests
import argparse
 
# List of individual node directories
node_dirs = [
    "/home/stratos1/rsnode1",
    "/home/stratos1/rsnode2",
    "/home/stratos1/rsnode3",
    "/home/stratos1/rsnode4",
    "/home/stratos1/rsnode5"
]

meta_nodes = [
    "stsds1ypxg8sj5vn4s4v0w965g4r9g3pt3vlz6wyzx0f", 
    "stsds14yhh6duc40n3l3y3qxt0vetm9numlstlxxfz05", 
    "stsds1z96pm5ls0ff2y7y8adpy6r3l8jqeaud7envnqv",
    "stsds129ffpumtwpnm25s2h63gfc9tc3ywl3srgg5mt7",
    "stsds1fxdk4cwm5nja6exxdey69pqqrj5tlnmysj2fwu",
    "stsds1793jm44fj9tw0c9c8gxwymc6dtnefw0u9p22wk",
    "stsds10kmygjv7e2t39f6jka6445q20e9lv4a7u3qex3"
]

titles = [
    "Activation",
    "Registration Status",
    "Mining",
    "Initial tier",
    "Ongoing tier",
    "Weight score",
    "Meta node"
]

def createArgs():

    args = argparse.ArgumentParser()
    args.add_argument ('-i', '--ip', type=str)
    args.add_argument ('-n', '--name', type=str)
    args.add_argument ('-u', '--url', type=str)
    args.add_argument ('-t', '--token', type=str)
    args.add_argument ('-c', '--chatID', type=str)

    # If you want to run the 'status.py' script on your server without passing parameters, 
    # then use these lines and specify the data for telegram
    #
    # args.add_argument ('-u', '--url', type=str, default = 'https://api.telegram.org/bot')
    # args.add_argument ('-t', '--token', type=str, default = 'YOUR_TOKEN_TG')
    # args.add_argument ('-c', '--chatID', type=str, default = 'YOUR_CHATID_TG')
 
    return args
 
def get_node_status(node_dir):

    status_output = ""
    status_text = ""

    # Save the original directory
    original_dir = os.getcwd()
    
    # Change to the node directory
    os.chdir(node_dir)
    
    # Start the ppd terminal
    child = pexpect.spawn('ppd terminal', encoding='utf-8')
    
    # Suppress the log file output
    child.logfile = open(os.devnull, 'w')
    
    # Wait for the prompt
    child.expect('> ')
    
    # Send the status command
    child.sendline('status')

    # Capture the status output and wait for the prompt again
    while True:
        try:
            status_output += child.read_nonblocking(size=1024, timeout=1)
        except pexpect.TIMEOUT as e:
            break

    child.expect('> ')
    
    # Send the exit command
    child.sendline('exit')
    
    # Ensure the exit command has completed
    child.expect(pexpect.EOF)
    
    # Close the log file
    child.logfile.close()
    
    # Change back to the original directory
    os.chdir(original_dir)
    
    # Extract the relevant status information
    status_start = status_output.rfind("Activation:")
        
    if status_start != -1:
        status_text = status_output[status_start:].strip()
    else:
        status_text = "404"

    return status_text

def parse_status(status_text):

    status_dict = {}

    if status_text == "404":
        for title in titles:
            status_dict[title] = "Not found"
        status_dict['Status'] = False        
    elif status_text == "":
        for title in titles:
            status_dict[title] = "No data"
        status_dict['Status'] = False
    else:    
        lines = status_text.split("|")
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                if 'Meta node' in key:
                    for sp in meta_nodes:
                        if sp in value:
                            value = sp[:7] + "..." + sp[-7:]
                status_dict[key.strip()] = value.strip()
        status_dict['Status'] = True
    return status_dict

def read_config(
    node_dir,
    key,
    value
):
    config_path = os.path.join(node_dir, 'config', 'config.toml')
    with open(config_path, 'r') as f:
        config = toml.load(f)
    output = config[key][value]

    return output
    

def get_storage_path_size(node_dir):

    storage_path = read_config(node_dir, 'home', 'storage_path')    
    
    # Calculate the size of the storage_path directory
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(storage_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    
    # Convert size to gigabytes
    size_gb = total_size / (1024 ** 3)
    
    return size_gb

def get_info_about_rewards(
     node_dir   
):
    wallet_address = read_config(node_dir, 'keys', 'wallet_address')
    url = f"https://rest.thestratos.org/stratos/pot/v1/rewards/wallet/{wallet_address}"

    response = requests.get(url)
    
    result = {}
    if response.status_code == 200:
        data = response.json()
        if "rewards" in data:        
            for key,values in data['rewards'].items():
                if key == "mature_total_reward":
                    for reward in values:                            
                        result['Mature_reward'] = "{0:.2f}".format(float(reward['amount']) / pow(10,18)) 
                if key == "immature_total_reward":
                    for reward in values: 
                        result['Immature_reward'] = "{0:.2f}".format(float(reward['amount']) / pow(10,18))   
    else:
        print(f"Error: no response from server {response.status_code}")
        result['Mature_reward'] = "No data"
        result['Immature_reward'] = "No data"

    return result

def sent_msg_to_tg_channel(
    msg
):
    params = {'chat_id': args.chatID,'text': msg, 'parse_mode': 'Markdown'}
    response = requests.get(args.url +args.token + '/sendMessage', params=params)

def formated_for_tg(
        status_nodes
):
    if args.ip == None and args.name == None:
        command = 'curl ifconfig.co'
        pipe = os.popen(command)
        ip = pipe.read()
        user = getpass.getuser()
        result = f"\nServer IP: {ip}" + f"Server Name: {user}\n\n" 
    else:
        result = f"\nServer IP: {args.ip}\n" + f"Server Name: {args.name}\n\n"

    for node in status_nodes:
        if node['Status'] != True:
            result += f"Node name: {node['Node']}\n"
            for title in titles:
                result += f"{title}: {node[title]}, check the logs...\n"
        else:
            result += f"Node name: {node['Node']}\n"
            if "Active" in node['Activation']:
                result += f"Activation: *{node['Activation']}* \U00002705\n"
            else:
                result += f"Activation: *{node['Activation']}* \U0000274C\n"
            if "Registered" in node['Registration Status']:
                result += f"Registration Status: _{node['Registration Status']}_\n"
            else:
                result += f"Registration Status: _{node['Registration Status']}_\n"
            if "ONLINE" in node['Mining']:
                result += f"Mining: *{node['Mining']}* \U0001F49A\n"
            elif "MAINTENANCE" in node['Mining']:
                result += f"Mining: *{node['Mining']}* \U0001F6E0\n"
            else:
                result += f"Mining: *{node['Mining']}* \U0001F494\n"
            if int(node['Initial tier']) == 2:
                result += f"Initial tier: {node['Initial tier']}\n"
            else:
                result += f"Initial tier: {node['Initial tier']}\n"
            if int(node['Ongoing tier']) == 2:
                #result += "Ongoing tier: " + "*" + node["Ongoing tier"] + "*" + " " + u'\U0001F315' + "\n"
                result += f"Ongoing tier: *{node['Ongoing tier']}* \U0001F7E2\n"
            else:
                result += f"Ongoing tier: *{node['Ongoing tier']}* \U0001F534\n"
            if int(node['Weight score']) >= 2000 and int(node['Ongoing tier']) == 2 and int(node['Weight score']) != 10000:
                result += f"Weight score: *{node['Weight score']}* \U00002B06\n"  
            elif int(node['Weight score']) == 10000 and int(node['Ongoing tier']) == 2:
                result += f"Weight score: *{node['Weight score']}* \U00002B06 \U0001F389\n"
            else:
                result += f"Weight score: *{node['Weight score']}* \U00002B07 \U0001F625\n"
            result += f"Meta: {node['Meta node']}\n"  
        result += f"Storage(Gb): {node['Stor(Gb)']}\n"
        if "No data" in node['Mature reward']:   
            result += f"Mature rewards: {node['Mature reward']} \U0001F937\n"
        else:
            result += f"Mature rewards: {node['Mature reward']}\U0001F4B0\n"
        if "No data" in node['Immature reward']: 
            result += f"Immature rewards: {node['Immature reward']} \U0001F937\n\n"
        else:
            result += f"Immature rewards: {node['Immature reward']}\U000023F3\n\n"
    return result

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    """
    Call in a loop to create a terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


if __name__ == '__main__':
    parser = createArgs()
    args = parser.parse_args()

# Collect the status of each node
status_data = []
total_nodes = len(node_dirs)
status_dict = {}
for i, node_dir in enumerate(node_dirs):
    status_text = get_node_status(node_dir)
    status_dict = parse_status(status_text)
    status_dict['Node'] = os.path.basename(node_dir)  # Add node name to the dictionary
    status_dict['Stor(Gb)'] = round(get_storage_path_size(node_dir), 2)  # Add storage size to the dictionary
    rewards = get_info_about_rewards(node_dir)
    status_dict['Mature reward'] = rewards['Mature_reward']
    status_dict['Immature reward'] = rewards['Immature_reward']
    status_data.append(status_dict)
   
    if i == (len(node_dirs) - 1):
        sent_msg_to_tg_channel(formated_for_tg(status_data))
        new_status_dict = {}
        new_status_data = []
        for status in status_data:
            new_status_dict = {key: value for key, value in status.items() if key != 'Status'}
            new_status_data.append(new_status_dict)

    # Update the progress bar
    print_progress_bar(i + 1, total_nodes, prefix='Progress:', suffix='Complete', length=50)

# Create a DataFrame
df = pd.DataFrame(new_status_data)

# Reorder the columns to make 'Node' the first column
columns_order = ['Node'] + [col for col in df.columns if col != 'Node']
df = df[columns_order]

# Shorten column names
df.rename(columns={
    'Activation': 'Activation',
    'Registration Status': 'Reg_Status',
    'Mining': 'Mining',
    'Initial tier': 'Init_T',
    'Ongoing tier': 'Ong_T',
    'Weight score': 'Weight',
    'Meta node': 'Meta',
    'Mature reward': 'Mature_Rew',
    'Immature reward': 'Immature_Rew'
}, inplace=True)

# Get the current working directory
current_directory = os.getcwd()

# Save the DataFrame to a CSV file in the current directory
output_file = os.path.join(current_directory, 'node_status.csv')
try:
    df.to_csv(output_file, index=False, sep=',')
    print(f"\nCSV file '{output_file}' has been written successfully.")
except Exception as e:
    print(f"\nAn error occurred while writing the CSV file: {e}")
 
# Print the DataFrame as a nicely formatted table using tabulate
print("\nNode status consolidated into node_status.csv\n")
print(">>>>>")
print(tabulate(df, headers='keys', tablefmt='plain'))
print(">>>>>\n")






