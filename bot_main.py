from io import BytesIO
from datetime import date
import time
from hackaton_api import synthesis_text
from utils import wav_to_mp3
from radio_api import radio_manager, radio_files
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
)
import locale

BOT_TOKEN = "2029640196:AAHJlZ2HfLubLOHM4fp_mycIrD3xrfepcWs"
HOST = 'perseus.shoutca.st'
USERNAME = 'urbantatar'
PASSWORD = 'c7rT6kYw11'

locale.setlocale(locale.LC_ALL, ('RU','UTF8'))
radio_manager = radio_manager(f'https://{HOST}', USERNAME, PASSWORD)
radio_files = radio_files(HOST, USERNAME, PASSWORD)

def handleNews(update, context):
    message = update.message.text[8:].strip()
    loadingMesId = context.bot.send_message(chat_id=update.effective_chat.id, text="Идет загрузка...").message_id
    wavFile = synthesis_text(message)
    with BytesIO(wavFile) as wav:
        with wav_to_mp3(wav) as mp3:
            shortName = message[:min(20, len(message))]
            path = '/media/news/' + shortName + '_' + str(int(time.time())) + '.mp3'

            radio_files.upload_file(path, mp3)
            radio_manager.invokeMethod('playlist', {'action': 'add', 'playlist': '21519', 'trackpath': path, 'albumname': date.today().strftime('%d.%m.%Y'), 'artistname': 'Новости'})
            radio_manager.invokeMethod('reindex', {'intoplaylist': '21519'})
            mp3.seek(0)
            context.bot.send_audio(chat_id=update.effective_chat.id, audio=mp3, title=shortName, performer="UrbanTatar")
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=loadingMesId)

def handleSaying(update, context):
    message = update.message.text[10:].strip()
    loadingMesId = context.bot.send_message(chat_id=update.effective_chat.id, text="Идет загрузка...").message_id
    wavFile = synthesis_text(message)
    with BytesIO(wavFile) as wav:
        with wav_to_mp3(wav) as mp3:
            shortName = message[:min(20, len(message))]
            path = '/media/sayings/' + shortName + '_' + str(int(time.time())) + '.mp3'

            radio_files.upload_file(path, mp3)
            radio_manager.invokeMethod('playlist', {'action': 'add', 'playlist': '21520', 'trackpath': path, 'albumname': date.today().strftime('%d.%m.%Y'), 'artistname': 'Пословицы'})
            radio_manager.invokeMethod('reindex', {'intoplaylist': '21520',})
            mp3.seek(0)
            context.bot.send_audio(chat_id=update.effective_chat.id, audio=mp3, title=shortName, performer="UrbanTatar")
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=loadingMesId)

updater = Updater(BOT_TOKEN)

dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("addnews", handleNews))
dispatcher.add_handler(CommandHandler("addsaying", handleSaying))

updater.start_polling(allowed_updates=Update.MESSAGE)
updater.idle()