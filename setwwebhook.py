import telegram

TOKEN= "6149369057:AAFwx8G3CHGlxC2UyXnUV0FkLTKP6F5IBwk"
url="https://davron0703qwerty1234.pythonanywhere.com/webhook"
bot = telegram.Bot(TOKEN)

print(bot.set_webhook(url))