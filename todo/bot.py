import requests
from .settings import base_url
from telegram import (Update, InlineKeyboardButton,CallbackQuery,InlineKeyboardMarkup,InlineQuery)
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext



def start(update: Update, context: CallbackContext):
    '''start function'''
    chat_id = update.message.chat.id
    first_name = update.message.chat.first_name
    user = {
        'chat_id': chat_id,
        'first_name': first_name
    }
    username = update.message.chat.username
    if username is not None: user['username'] = username
    last_name = update.message.chat.last_name
    if last_name is not None: user['last_name'] = last_name

    url_for_register = f'{base_url}/create-user'
    response = requests.post(url_for_register, json=user)

    btn1=InlineKeyboardButton(text='Menu', callback_data="menu")
    keyboard=InlineKeyboardMarkup([[btn1]])
    update.message.reply_markdown_v2('*Hello, welcome to our bot\!*', reply_markup=keyboard)
    btn = KeyboardButton(text='my tasks')
    update.message.reply_markdown_v2(
        '*Hello, welcome to our bot\!*\n\n_select name for creating task_',
        reply_markup=ReplyKeyboardMarkup(keyboard=[[btn]]))
    
def menu(update: Update, context: CallbackContext):
    bot = context.bot
    query = update.callback_query

    chat_id = query.message.chat.id
    btn1=InlineKeyboardButton(text='Add tasks', callback_data="add_task")
    btn2=InlineKeyboardButton(text='Tasks', callback_data="get_task")
    btn3=InlineKeyboardButton(text='Delete task', callback_data="delete_task")
    keyboard=InlineKeyboardMarkup([[btn1],[btn2],[btn3]])
    bot.sendMessage(chat_id, "Menu:", reply_markup=keyboard)
def get_tasks(update: Update, context: CallbackContext):
    '''get tasks'''
    query = update.callback_query
    chat_id=query.message.chat.id
    data=requests.get(f'{base_url}/get-tasks/{chat_id}')
    data=data.json()
    keyboard = [[],[]]
    i=1
    text=''
    if data==[]:
        btn1 = InlineKeyboardButton(text="🏘 Bosh Menu", callback_data="bosh_menu")
        keyboard.append([btn1])
    '''add new task'''
    chat_id = update.message.chat.id

    url_for_get_tasks = f'{base_url}/get-tasks/{chat_id}'
    response = requests.get(url_for_get_tasks)

    msg = ''
    if response.status_code == 200:
        tasks = response.json()
        
        for task in tasks:
            btn = InlineKeyboardButton(text=task['name'], callback_data=task['name'])
            if task['done']:
                msg += f'✅ {task["name"]}\n'
            else:
                msg += f'❌ {task["name"]}\n'
        update.message.reply_html(msg)


        keyboard = InlineKeyboardMarkup(keyboard)
        query.edit_message_text( 'Empty \n', reply_markup=keyboard)
    for task in data :
        task_taxt=task['name']
        text+=f'{i}. {task_taxt} \n'
        btn = InlineKeyboardButton(
            text=f'{i}. ❌',
            callback_data=f"task_{i}"
        )
        if i < 6:
            # 1 2 3 4 5
            keyboard[0].append(btn)
        else:
            # 6 7 8 9 10
            keyboard[1].append(btn)

        i+=1
    btn1 = InlineKeyboardButton(text="🏘 Bosh Menu", callback_data="bosh_menu")
    keyboard.append([btn1])

    keyboard = InlineKeyboardMarkup(keyboard)
    query.edit_message_text( text=text, reply_markup=keyboard)
def write_task(update: Update, context: CallbackContext):
    bot = context.bot
    query = update.callback_query
    chat_id=query.message.chat.id
    bot.sendMessage(chat_id,"Write a task:")
def add_task(update: Update, context: CallbackContext):
    '''add new task'''
    bot = context.bot
    # query = update.callback_query
    # chat_id=query.message.chat.id
    chat_id=update.message.chat.id
    text=update.message.text
    url=f'{base_url}/create-task/{chat_id}'
    datf={'name': text}
    r=requests.post(url=url, json=datf)
    bot.sendMessage(chat_id, 'added task✅')
    return r
def delete_task(update: Update, context: CallbackContext):
    '''add new task'''
    query = update.callback_query
    chat_id=query.message.chat.id
    url=f'{base_url}/delete-task/{chat_id}'
    data=requests.post(url=url)
    query.answer("Done✅")
    

def mark(update: Update, context: CallbackContext):
    '''add new task'''
    query = update.callback_query
    task_id=query.data.split('_')[-1]
    query = update.callback_query
    chat_id=query.message.chat.id
    r=requests.post(f'{base_url}/mark-task/{chat_id}/{task_id}')
    data=requests.get(f'{base_url}/get-tasks/{chat_id}')
    data=data.json()
    keyboard = [[],[]]
    i=1
    text=''
    if data==[]:
        btn1 = InlineKeyboardButton(text="🏘 Bosh Menu", callback_data="bosh_menu")
        keyboard.append([btn1])

        keyboard = InlineKeyboardMarkup(keyboard)
        query.edit_message_text( 'Empty \n', reply_markup=keyboard)
    for task in data :
        task_taxt=task['name']
        if task['done']==True:
            text+=f'{i}. {task_taxt} \n'
            btn = InlineKeyboardButton(

                text=f'{i}. ✅',
                callback_data=f"task_{i}"
            )
        else:
            text+=f'{i}. {task_taxt} \n'
            btn = InlineKeyboardButton(

                text=f'{i}. ❌',
                callback_data=f"task_{i}"
            )
        if i < 6:
            # 1 2 3 4 5
            keyboard[0].append(btn)
        else:
            # 6 7 8 9 10
            keyboard[1].append(btn)

        i+=1
    btn1 = InlineKeyboardButton(text="🏘 Bosh Menu", callback_data="bosh_menu")
    keyboard.append([btn1])

    keyboard = InlineKeyboardMarkup(keyboard)
    query.edit_message_text( text=text, reply_markup=keyboard)

