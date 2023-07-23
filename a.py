import requests
import time
import threading
import keyboard
import PySimpleGUI as sg
from colorama import Fore, init

init(autoreset=True)

def get_servers(token):
    url = "https://discord.com/api/v9/users/@me/guilds"
    headers = {
        "Authorization": token
    }
    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        return r.json()
    return []

def get_common_servers(tokens):
    common_servers = set()
    valid_tokens = [token for token in tokens if check_token(token)]
    if not valid_tokens:
        return common_servers

    server_lists = [get_servers(token) for token in valid_tokens]

    if len(server_lists) == 1:
        return set(server['name'] for server in server_lists[0])

    common_servers = set(server_lists[0][0]['name'])
    for i in range(1, len(server_lists)):
        common_servers.intersection_update(server['name'] for server in server_lists[i])

    return common_servers

def select_server_gui(common_servers):
    layout = [[sg.Text('Select a server:', background_color='#222', text_color='white')],
              [sg.Listbox(values=list(common_servers), size=(40, 10), background_color='#222', text_color='white', select_mode='LISTBOX_SELECT_MODE_SINGLE')],
              [sg.Button('OK', button_color=('white', 'red')), sg.Button('Cancel', button_color=('white', 'red'))]]

    window = sg.Window('Server Selection', layout, background_color='#222')

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            window.close()
            return None
        elif event == 'OK':
            server_name = values[0][0]
            window.close()
            return server_name

def get_server_id(token, server_name):
    url = "https://discord.com/api/v9/users/@me/guilds"
    headers = {
        "Authorization": token
    }
    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        servers = r.json()
        for server in servers:
            if server['name'] == server_name:
                return server['id']
    return None

def get_channel_id(token, server_id):
    url = f"https://discord.com/api/v9/guilds/{server_id}/channels"
    headers = {
        "Authorization": token
    }
    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        channels = r.json()
        layout = [[sg.Text('Select a channel:', background_color='#222', text_color='white')],
                  [sg.Listbox(values=[f"{channel['name']} ({channel['id']})" for channel in channels], size=(50, 10), background_color='#222', text_color='white', select_mode='LISTBOX_SELECT_MODE_SINGLE')],
                  [sg.Button('OK', button_color=('white', 'red')), sg.Button('Cancel', button_color=('white', 'red'))]]

        window = sg.Window('Channel Selection', layout, background_color='#222')

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Cancel':
                window.close()
                return None
            elif event == 'OK':
                selected_channel = values[0][0]
                channel_id = selected_channel.split(" ")[-1][1:-1]  # Extract channel ID from the selected item
                window.close()
                return channel_id

def send_message_to_channel(server_id, channel_id, token, message):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    payload = {
        "content": message
    }

    masked_token = '*' * 7 + token[7:]
    while not keyboard.is_pressed('q'):
        time_now = time.strftime("%Y-%m-%d %H:%M:%S")
        formatted_time = Fore.CYAN + f"{time_now}"
        r = requests.post(url, headers=headers, json=payload)
        if r.status_code == 200:
            print(f"{formatted_time} : {Fore.GREEN}Sent {Fore.MAGENTA} = {masked_token}")
        else:
            print(f"{formatted_time} : {Fore.RED}Failed {Fore.MAGENTA} = {masked_token}")

        time.sleep(0.03)

def check_token(token):
    headers = {"Authorization": token.encode("utf-8")}
    r = requests.get("https://discordapp.com/api/v9/users/@me/library", headers=headers)
    return r.status_code == 200

def create_default_message_file():
    default_message = "The server was spammed by Blaze."
    with open('message.txt', 'w') as message_file:
        message_file.write(default_message)

def main():
    print("                                               ____  _               ")
    print("                                              | __ )| | __ _ _______ ")
    print("                                              |  _ \| |/ _` |_  / _ \\")
    print("                                              | |_) | | (_| |/ /  __/")
    print("                                              |____/|_|\__,_/___\___| ")
    print("\n" * 3)

    with open('tokens.txt', 'r') as token_file:
        tokens = token_file.read().splitlines()

    common_servers = get_common_servers(tokens)
    if not common_servers:
        print("No common servers found.")
        return

    selected_server = select_server_gui(common_servers)
    if selected_server is None:
        return

    server_id = get_server_id(tokens[0], selected_server)
    if not server_id:
        print("Failed to get server ID.")
        return

    channel_id = get_channel_id(tokens[0], server_id)
    if not channel_id:
        print("Failed to get channel ID.")
        return

    if not open('message.txt', 'r').read():
        print("Creating 'message.txt' with default message...")
        create_default_message_file()

    with open('message.txt', 'r') as message_file:
        message = message_file.read()

    valid_tokens = [token for token in tokens if check_token(token)]

    if not valid_tokens:
        print("No valid tokens found in tokens.txt.")
        return

    threads = []
    for token in valid_tokens:
        thread = threading.Thread(target=send_message_to_channel, args=(server_id, channel_id, token, message))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
