import os
import json
import requests
import logging

import pyrogram
from pyrogram import Client, filters, idle
from pyrogram.handlers import MessageHandler
from requests.models import Response


TOKEN = os.environ.get("BOT_TOKEN")
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
OWNER_ID = os.environ.get("OWNER_ID")
# optional
IMG_URL = os.environ.get("IMG_URL")

# logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('quotlog.txt'), logging.StreamHandler()],
                    level=logging.DEBUG) # change debug to lnfo if needed

logging.getLogger("pyrogram").setLevel(logging.INFO) # change logging.INFO to logging.WARNING to filter out INFO level for pyrogram

LOGGER = logging.getLogger(__name__)

app = Client(
        ':memory:',
        bot_token=TOKEN,
        api_id=API_ID,
        api_hash=API_HASH
    )

def log_msg_info(client, message):
    LOGGER.info('UID: {} - UN: {} - MSG: {}'.format(message.from_user.id, message.chat.username, message.text))

def get_zen_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = "<i>" + json_data[0]['q'] + "</i>" + "\n\n - " + "<b>" + json_data[0]['a'] + "</b>"    
    except Exception as ex: # as ex meant for future exception template
        LOGGER.error("something went wrong while retrieving a quote. traceback:")
        LOGGER.error(ex)
        quote = "something went wrong while retrieving a quote. \n\ntraceback: \n" + "<i>" + f"{ex}" + "</i>"
    return(quote)

def q(client, message):
    log_msg_info(client, message)
    quote = get_zen_quote()
    message.reply_text(
        quote,
        quote=True
    )

def log(client, message):
    log_msg_info(client, message)   
    with open('quotlog.txt', 'rb') as f:
        app.send_document(document=f,
                          reply_to_message_id=message.message_id,
                          chat_id=message.chat.id)

def start(client, message):
    log_msg_info(client, message)
    replyPMMessage = "Hehe, Just another Quote Bot. \nHit /help to see a list of commands! \n\nAPI -> zenquotes.io \n\nDev -> @MizuharaChizru \n\nModified by -> @orsixtyone"
    replyGPMessage = "I sensed that you're using this bot in a group." # comment if useless, 
    if message.chat.type == "private":
        if IMG_URL is not None:
            message.reply_photo(photo=IMG_URL, caption=replyPMMessage, quote=True)
        else:
            message.reply_text(replyPMMessage, quote=True)
    if message.chat.type == "group":
        message.reply_text(replyGPMessage, quote=True)


def help(client, message):
    log_msg_info(client, message)
    helpMessage = """
    Here's Help:\n\n> /start - **bruh you already tried that** \n> /help - **don't do dis** \n> /quote - **get motivated** :) \n> /q - **motivated you'll get** \n> /log - **get log** __[owner only]__
    """
    message.reply_text(helpMessage, quote=True)

def nan(client, message):
    log_msg_info(client, message)

    
if __name__ == "__main__":
    app.start()
    buns = "@" + app.get_me().username
    # start msg
    incom_start_message = MessageHandler(
        start,
        filters=filters.command(['start', 'start' + buns])
    )
    app.add_handler(incom_start_message)
    # help msg
    incom_help_message = MessageHandler(
        help,
        filters=filters.command(['help', 'help' + buns])
    )
    app.add_handler(incom_help_message)
    # quote msg
    incom_quote_msg = MessageHandler(
        q,
        filters=filters.command(['quote', 'q', 'quote' + buns, 'q' + buns])
    )
    app.add_handler(incom_quote_msg)
    # log msg
    incom_log_msg = MessageHandler(
        log,
        filters=filters.command(['log', 'log' + buns])
        & filters.user(users=OWNER_ID)
    )
    app.add_handler(incom_log_msg)
    # for other msgs
    incom_nan_msg = MessageHandler(
        nan
    )
    app.add_handler(incom_nan_msg)
    LOGGER.info("Bot Started!")
    idle()
