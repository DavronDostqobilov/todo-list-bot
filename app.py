from flask import Flask, request
from telegram import Update
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler,Dispatcher
from todo import (
    start,
    get_tasks,
    add_task,
    delete_task,
    mark,
    menu,
    write_task,
)
TOKEN ="6149369057:AAFwx8G3CHGlxC2UyXnUV0FkLTKP6F5IBwk"
bot = telegram.Bot(TOKEN)

app = Flask(__name__)
@app.route("/")
def ishladi():
    return "Bot ishladi"


@app.route("/webhook", methods=["POST"])
def home():
    dp = Dispatcher(bot, None, workers=0)
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)

    # handlers
    dp.add_handler(CommandHandler(['start', 'boshlash'], start))
    dp.add_handler(CallbackQueryHandler(get_tasks, pattern='get_task'))
    dp.add_handler(CallbackQueryHandler(write_task, pattern='add_task'))
    dp.add_handler(CallbackQueryHandler(delete_task, pattern='delete_task'))
    dp.add_handler(CallbackQueryHandler(mark, pattern='task'))
    dp.add_handler(CallbackQueryHandler(menu, pattern='bosh_menu'))
    dp.add_handler(CallbackQueryHandler(menu, pattern='menu'))
    dp.add_handler(MessageHandler(Filters.text, add_task))
    return 'ok'

if __name__ == '__main__':
    app.run(debug=True)