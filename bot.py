# import logging
# from telegram import Update
# from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )

# logger = logging.getLogger(__name__)

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

# async def set_learning_goal(update: Update, context:ContextTypes.DEFAULT_TYPE):
#     #To implement
#     await context.bot.send_message(chat_id=update.effective_chat.id, text="What are your learning goals?")

# async def learning_goals_setter(message):
#     goals = message
#     print(message)
#     await context.bot.send_message(chat_id=update.effective_chat.id, text="Gotcha!")

# async def match(update: Update, context:ContextTypes.DEFAULT_TYPE):
#     #To implement
#     await context.bot.send_message(chat_id=update.effective_chat.id, text="Starting the matching process...")

# def error(update, context):
#     """Log Errors caused by Updates."""
#     logger.warning('Update "%s" caused error "%s"', update, context.error)

# if __name__ == '__main__':
#     application = ApplicationBuilder().token('6233481401:AAHrhtvZ9ivUdCS-jjiq2f6IeSusyg7ZKPI').build()
    
#     start_handler = CommandHandler('start', start)
#     set_learning_goals_handler = CommandHandler('setgoals', set_learning_goal)
#     match_handler = CommandHandler('match', match)
#     application.add_handler(start_handler)
#     application.add_handler(set_learning_goals_handler)
#     application.add_handler(match_handler)
#     application.add_error_handler(error)
    
#     application.run_polling()

#     Done! Congratulations on your new bot. You will find it at t.me/learningbuddies_bot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.

# Use this token to access the HTTP API:
# 6233481401:AAHrhtvZ9ivUdCS-jjiq2f6IeSusyg7ZKPI
# Keep your token secure and store it safely, it can be used by anyone to control your bot.

# For a description of the Bot API, see this page: https://core.telegram.org/bots/api

import telebot
import logging

bot = telebot.TeleBot("6233481401:AAHrhtvZ9ivUdCS-jjiq2f6IeSusyg7ZKPI")
# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

#link to firestore
import firebase_admin

cred_object = firebase_admin.credentials.Certificate('~/Downloads/learningbuddies-f71a2-b475d9c8d067.json')
default_app = firebase_admin.initialize_app(cred_object, {
	'databaseURL': 'https://learningbuddies-f71a2-default-rtdb.asia-southeast1.firebasedatabase.app/'
	})

from firebase_admin import db


#To add to database
users = {}
num_users = 0
ref = db.reference('learningbuddies-f71a2-default-rtdb.asia-southeast1.firebasedatabase')

class User:
    def __init__(self, id, interests):
        self.id = id
        self.interests = interests

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to learningbuddies!")
    user_id = message.chat.id
    users[user_id] = User(user_id, [])

#To implement matching algo
@bot.message_handler(commands=['match'])
def match(message):
    bot.reply_to(message, "Starting the matching process...")
  
    


#Message format: /learning-goals React JavaScript TypeScript
@bot.message_handler(commands=["learning-goals"])
def learning_goals_setter(message):
    interests = message.text.split(" ")[1:]
    print(interests)
    users[message.chat.id].interests = interests
    print(users[message.chat.id].id)
    print(users[message.chat.id].interests)
    bot.reply_to(message, "What are your learning goals?")

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "Help Message")

# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")

bot.polling()
