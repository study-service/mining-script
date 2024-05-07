import socket
import requests
import json
import schedule
import time
import telebot
import ping3
import logging

# Configure logging
logging.basicConfig(filename='monitor_server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define Telegram bot token and chat ID
BOT_TOKEN = "7123548020:AAHc6NKOomO79VbAnLSV1VyMuTJahFfsRx0"
url = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates'
bot = telebot.TeleBot(BOT_TOKEN)
def check_server(ip, port):
    try:
        # # Create a TCP socket
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #     # Set timeout to 1 second
        #     s.settimeout(5)
        #     # Attempt to connect to the server
        #     s.connect((ip, port))
        response = ping3.ping(ip, timeout=2)
        if response is not None:
            return True
        else:
            return False
    except Exception as e:
        logging.warn(f"Error checking server {ip}:{port}: {e}")
        return False



def send_telegram_notification(chat_id, message):
    try:
        bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        logging.warn(f"Error sending notification: {e}")

def get_chat_id():
    response = requests.get(url)
    chat_id = response.json()['result'][0]['message']['chat']['id']
    return chat_id

def check_servers_and_notify():
    with open("server_info.json", "r") as file:
        server_data = json.load(file)
    chat_id = get_chat_id()
    # Iterate over each server and check its status
    for server in server_data:
        server_ip = server["ip"]
        server_port = int(server["port"])
        # Check if the server is active
        logging.info(f"Checking {server_ip}:{server_port}")
        if not check_server(server_ip, server_port):
            # Send notification to Telegram group if the server is not active
            message = f"Server at {server_ip}:{server_port} is down!"
            send_telegram_notification(chat_id, message)

if __name__ == "__main__":
    check_servers_and_notify()
    # Schedule the task to run every 5 minutes
    schedule.every(5).minutes.do(check_servers_and_notify)

    # Run the scheduler indefinitely
    while True:
        schedule.run_pending()
        time.sleep(1)
