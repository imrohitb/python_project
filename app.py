import telebot
import cv2
import time
import threading
import mysql.connector
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Initialize the Telegram bot
API_TOKEN = '7117496498:AAEBMWLQfwiAl0UvOV3FZchEadDiWOhHum0'
bot = telebot.TeleBot(API_TOKEN)

# Initialize MySQL database connection
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'atm_data'

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Create atm_data table
        cursor.execute('''CREATE TABLE IF NOT EXISTS atm_data (
                            atm_id VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci PRIMARY KEY,
                            rtsp_url VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci,
                            ip_data VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci
                          )''')
        
        # Create ip_data table
        cursor.execute('''CREATE TABLE IF NOT EXISTS ip_data (
                            atm_id VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci PRIMARY KEY,
                            ip_address VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci
                          )''')
        conn.commit()
        print("Database initialized successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()

def insert_atm_data(atm_id, rtsp_url, ip_data):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO atm_data (atm_id, rtsp_url, ip_data) VALUES (%s, %s, %s)", (atm_id, rtsp_url, ip_data))
        conn.commit()
        conn.close()
        return True
    except mysql.connector.IntegrityError:
        print(f"ATM ID '{atm_id}' already exists.")
        conn.close()
        return False

def insert_ip_data(atm_id, ip_address):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO ip_data (atm_id, ip_address) VALUES (%s, %s)", (atm_id, ip_address))
        conn.commit()
        conn.close()
        return True
    except mysql.connector.IntegrityError:
        print(f"ATM ID '{atm_id}' already exists in the IP data.")
        conn.close()
        return False

def get_rtsp_url(atm_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT rtsp_url FROM atm_data WHERE atm_id=%s", (atm_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_ip_address(atm_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ip_address FROM ip_data WHERE atm_id=%s", (atm_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

current_chat_rtsp_url = None
is_bot_alive = True

def send_photo_from_rtsp(chat_id, rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)
    sent_photos = set()

    ret, frame = cap.read()
    if ret:
        # Convert the frame to JPEG
        _, img_encoded = cv2.imencode('.jpg', frame)
        img_bytes = img_encoded.tobytes()

        # Send the image to the Telegram chat only if it hasn't been sent before
        if img_bytes not in sent_photos:
            bot.send_photo(chat_id=chat_id, photo=img_bytes)
            sent_photos.add(img_bytes)

    cap.release()

# Handler for the /start command
@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.reply_to(message, "Please send me the ATM ID.")
    global current_chat_rtsp_url
    current_chat_rtsp_url = None

# Handler for processing user messages
@bot.message_handler(func=lambda message: True)
def echo_all(message: Message):
    global current_chat_rtsp_url

    text = message.text.lower()

    if text == '/stop':
        current_chat_rtsp_url = None
        bot.reply_to(message, "RTSP stream stopped.")
        return

    if text == '/list':
        atm_ids = get_all_atm_ids()
        if atm_ids:
            bot.reply_to(message, f"Existing ATM IDs: {', '.join(atm_ids)}")
        else:
            bot.reply_to(message, "No ATM IDs found in the database.")
        return

    atm_id = message.text
    rtsp_url = get_rtsp_url(atm_id)
    ip_address = get_ip_address(atm_id)

    if rtsp_url is not None:
        if ip_address is not None:
            if current_chat_rtsp_url is not None and current_chat_rtsp_url != rtsp_url:
                bot.reply_to(message, "You are already receiving images from another RTSP stream. Please stop it first.")
            else:
                bot.reply_to(message, "ATM ID valid. Sending one image from RTSP stream.")
                current_chat_rtsp_url = rtsp_url
                # Start capturing images in a separate thread
                threading.Thread(target=send_photo_from_rtsp, args=(message.chat.id, current_chat_rtsp_url)).start()
        else:
            bot.reply_to(message, "IP address not found for the ATM ID.")
    else:
        print(f"ATM ID '{atm_id}' not found.")
        bot.reply_to(message, "Invalid ATM ID. Please try again.")

# Handler for checking if the bot is alive
@bot.message_handler(commands=['alive'])
def alive_handler(message: Message):
    global is_bot_alive
    if is_bot_alive:
        bot.reply_to(message, "Bot is running.")
    else:
        bot.reply_to(message, "Bot is not running.")

# Handler for adding ATM IDs and RTSP URLs via bot
@bot.message_handler(commands=['add'])
def add_atm_id_and_rtsp_url_via_bot_handler(message: Message):
    bot.reply_to(message, "Please send the ATM ID, RTSP URL, and IP data separated by spaces.")

    def handle_add_atm_id_and_rtsp_url(message: Message):
        atm_id, rtsp_url, ip_data = message.text.split()
        if insert_atm_data(atm_id, rtsp_url, ip_data):
            bot.reply_to(message, f"ATM ID '{atm_id}', RTSP URL '{rtsp_url}', and IP data '{ip_data}' added to the database.")
        else:
            bot.reply_to(message, f"ATM ID '{atm_id}' already exists in the database.")

    bot.register_next_step_handler(message, handle_add_atm_id_and_rtsp_url)

# Handler for adding ATM IPs via bot
@bot.message_handler(commands=['addip'])
def add_atm_ip_via_bot_handler(message: Message):
    bot.reply_to(message, "Please send the ATM ID and IP address separated by a space.")

    def handle_add_atm_ip(message: Message):
        atm_id, ip_address = message.text.split()
        if insert_ip_data(atm_id, ip_address):
            bot.reply_to(message, f"ATM ID '{atm_id}' and IP address '{ip_address}' added to the database.")
        else:
            bot.reply_to(message, f"ATM ID '{atm_id}' already exists in the IP data.")

    bot.register_next_step_handler(message, handle_add_atm_ip)

# Initialize the database
initialize_database()

# Start the bot
bot.polling(none_stop=True)
