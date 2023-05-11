from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from todo import (
    start,
    get_tasks,
    add_task,
    delete_task,
    mark,
    menu,
    write_task,
)
import os

TOKEN = os.environ.get('TOKEN')


def main():
    # updater obj
    updater = Updater(token=TOKEN)

    # dispetcher obj
    dp = updater.dispatcher

    # handlers
    dp.add_handler(CommandHandler(['start', 'boshlash'], start))
    dp.add_handler(CallbackQueryHandler(get_tasks, pattern='get_task'))
    dp.add_handler(CallbackQueryHandler(write_task, pattern='add_task'))
    dp.add_handler(CallbackQueryHandler(delete_task, pattern='delete_task'))
    dp.add_handler(CallbackQueryHandler(mark, pattern='task'))
    dp.add_handler(CallbackQueryHandler(menu, pattern='bosh_menu'))
    dp.add_handler(CallbackQueryHandler(menu, pattern='menu'))
    dp.add_handler(MessageHandler(Filters.text, add_task))

    

    # polling started
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()