import concurrent.futures
import subprocess
import re
import sys
import time
import traceback
from datetime import datetime
import pexpect
import telebot
import requests

BOT_TOKEN = "7123548020:AAHc6NKOomO79VbAnLSV1VyMuTJahFfsRx0"
url = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates'
bot = telebot.TeleBot(BOT_TOKEN)
def register_hotkey(subnet_id, wallet, hotkey, highest_cost, password):
    response = requests.get(url)
    chat_id = response.json()['result'][0]['message']['chat']['id']

    try:
        command = 'btcli s register -subtensor.network finney --netuid {} --wallet.name {} --wallet.hotkey {}'.format(subnet_id, wallet, hotkey)
        # Get the current time
        current_time = datetime.now().time()

        # Format the time as HH:MM:SS
        formatted_time = current_time.strftime("%H:%M:%S")

        # Print the formatted time
        print("\nColdkey:", wallet, "Hotkey:", hotkey, flush=True)
        print(formatted_time, flush=True)

        child = pexpect.spawn(command)

        child.logfile_read = sys.stdout.buffer

        child.expect('Enter subtensor network', 10000)
        print("\nSending: <enter>", flush=True)
        child.sendline('')

        child.expect('The cost to register by recycle is (.*?)(?:\\n|$)', 100000)
        cost_str = child.match.group(1).decode('utf-8').replace('τ', '')
        clean_cost_str = re.sub(r'\x1b\[[0-9;]*m', '', cost_str).strip()
        cost = float(clean_cost_str)

        if cost > highest_cost:
            print("Not buying: n", flush=True)
            child.sendline('n')

        else:
            print(f"Sending1 {hotkey}: y", flush=True)
            child.sendline('y')

        child.expect('Enter password to unlock key')
        print(f"\nSending {hotkey}: password")
        child.sendline(password)
        print(f"\nPassword {hotkey} sent")
        try:
            child.expect('Recycle (.*?) to register on subnet', 100000)
        except Exception as e1:
            print(f"Error recycle {hotkey}", e1)
            return
        recycle_cost_str = child.match.group(1).decode('utf-8').replace('τ', '')
        clean_recycle_cost_str = re.sub(r'\x1b\[[0-9;]*m', '', recycle_cost_str).strip()
        recycle_cost = float(clean_recycle_cost_str)
        print("Recycle cost:", recycle_cost)

        if recycle_cost > highest_cost:
            print("Sending cancel register: n", flush=True)
            child.sendline('n')
        else:
            print("Sending2: y", flush=True)
            child.sendline('y')
            try:
                child.expect('Registered', 100000)
                print(f"register subnet {subnet_id} hotkey {hotkey} success")
                bot.send_message(chat_id=chat_id, text=f"register subnet {subnet_id} wallet {wallet} hotkey {hotkey} success cost:{recycle_cost}")
            except Exception as e2:
                print(f"An error 1 occurred register ${subnet_id} hotkey ${hotkey}", e2)

    except Exception as e:
        print(f"An error occurred register {subnet_id} hotkey {hotkey}", e)
        print(traceback.format_exc())
        child.sendintr()  # Send Ctrl+C
        child.expect(pexpect.EOF)  # Wait for the command to exit

def register_keys(subnet_id, wallet, hotkeys, highest_cost, password):
    # Create ThreadPoolExecutor
    while True:

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit tasks for each hotkey registration
            futures = [executor.submit(register_hotkey, subnet_id, wallet, hotkey, highest_cost, password) for hotkey in hotkeys]

            # Wait for all tasks to complete
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
            print("All hotkeys registered successfully:", all(results))

# Define your inputs
subnet_id = 12
wallet_name = "nta"
hotkey_names = ["h7"]  # a list with the names of all the hotkeys you want to register
max_cost = 0.09  # The maximal amount of Tao you are willing to burn to register
coldkey_password = "anh201297@"  # Password for your cold key

# Call the method to register the keysgi
register_keys(subnet_id, wallet_name, hotkey_names, max_cost, coldkey_password)