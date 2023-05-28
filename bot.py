import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def set_learning_goal(update: Update, context:ContextTypes.DEFAULT_TYPE):
    #To implement
    await context.bot.send_message(chat_id=update.effective_chat.id, text="What are your learning goals?")

async def match(update: Update, context:ContextTypes.DEFAULT_TYPE):
    #To implement
    await context.bot.send_message(chat_id=update.effective_chat.id)

if __name__ == '__main__':
    application = ApplicationBuilder().token('6233481401:AAHrhtvZ9ivUdCS-jjiq2f6IeSusyg7ZKPI').build()
    
    start_handler = CommandHandler('start', start)
    set_learning_goals_handler = CommandHandler('setgoals', set_learning_goal)
    match_handler = CommandHandler('match', match)
    application.add_handler(start_handler)
    application.add_handler(set_learning_goals_handler)
    application.add_handler(match_handler)
    
    application.run_polling()

#     Done! Congratulations on your new bot. You will find it at t.me/learningbuddies_bot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.

# Use this token to access the HTTP API:
# 6233481401:AAHrhtvZ9ivUdCS-jjiq2f6IeSusyg7ZKPI
# Keep your token secure and store it safely, it can be used by anyone to control your bot.

# For a description of the Bot API, see this page: https://core.telegram.org/bots/api
