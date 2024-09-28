import requests
from telegram.constants import ParseMode
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Replace with your Telegram bot token
TELEGRAM_BOT_TOKEN = '6327652527:AAHp0SR2h7PKPIIrQqp5ij_jNnsUQBNk41U'
# Replace with your Telegram chat ID
TELEGRAM_CHAT_ID = '4177454438'

def ping(strip):
    try:
        response = requests.get(f"http://www.google.com/search?q={strip}", timeout=1)
        return response.status_code == 200
    except requests.RequestException:
        return False

def send_telegram_message(bot, chat_id, message):
    bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.MARKDOWN)

def ping_system(context: CallbackContext):
    for int_row in range(2, 65536):
        strip = "your_strip"  # Replace with the actual IP or domain to ping
        if ping(strip):
            print(f"{strip} is online")
            # Add your online status handling here

        else:
            print(f"{strip} is offline")
            # Add your offline status handling here

            # Send Telegram Message
            str_message = f"Ping {strip} is Offline"
            send_telegram_message(context.bot, TELEGRAM_CHAT_ID, str_message)

        context.job_queue.run_once(ping_system, interval=30)  # Run again after 30 seconds

def start(update: Update, context: CallbackContext) -> None:
    context.job_queue.run_once(ping_system, 0)  # Start the job immediately

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
