import telebot
import logging
import os
import json

bot = telebot.TeleBot("6233481401:AAHrhtvZ9ivUdCS-jjiq2f6IeSusyg7ZKPI")
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

#link to firestore
import firebase_admin

dir = os.path.dirname(__file__)
filename = os.path.join(dir,'servicekey.json' )
cred_object = firebase_admin.credentials.Certificate(filename)
default_app = firebase_admin.initialize_app(cred_object, {
	'databaseURL': 'https://learningbuddies-f71a2-default-rtdb.asia-southeast1.firebasedatabase.app/'
	})

from firebase_admin import db

class User:
    def __init__(self, id, plan, partnerid):
        self.id = id
        self.plan = None
        self.partnerid = None
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def fromJSON(dict):
        return User(dict["id"], dict["plan"], dict["partnerid"])

class PlanProgress:
    def __init__(self, uid, plan, progress, currtask, iscomplete):
        self.uid = uid
        self.plan = plan
        self.progress = ""
        self.currtask = 0
        self.iscomplete = False
    def getprogress():
        text_file = open('learn-angular.txt','r')
        Lines = text_file.readlines()
        line_arr = []
        for line in Lines:
            task = line.split("|")
            line_arr.append(task)
        text_file.close()
        return line_arr
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def fromJSON(dict):
        return PlanProgress(dict["uid"], dict["plan"], dict["progress"],
            dict["iscomplete"])
        
#To add to database
# usersRef = db.reference('users')
# usersJSON = usersRef.get()
#load users JSON to users dict
# users = {}
# for userJSON in usersJSON:
#     users[userJSON] = User.fromJSON(json.loads(usersJSON[userJSON]))
# num_users = 0
plan_codes = ["learn-angular", "learn-react", "75-hard", "couch25k"]

#HAVE TO execute before all other commands to register uid        
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to learningbuddies!")
    user_id = message.chat.id
    # users[user_id] = User(user_id, None)
    # user_obj = users[user_id].toJSON()
    new_ref = db.reference('users')
    new_ref.set({
    user_id : {
        'plan': 'None',
        'partnerid': 'None'
    }})

#To implement matching algo
@bot.message_handler(commands=['match'])
def match(message):
    bot.reply_to(message, "Starting the matching process...")


@bot.message_handler(commands=['select-plan'])
def plan_selector(message):
    plan_code = message.text.split(" ")[1]
    if plan_code in plan_codes:
        curr_ref = db.reference('users/'+str(message.chat.id)+'/plan')
        curr_ref.set(plan_code)
        plan_ref = db.reference('plan-progress/' + str(message.chat.id) + "/" + plan_code)
        plan_ref.set({'plan-progress': PlanProgress.getprogress(), 'currtask': 0, 'iscomplete' : False})
        bot.reply_to(message, plan_code + " is now your current plan.")
    else:
        bot.reply_to(message, "I'm sorry. We currently do not have that plan!")

@bot.message_handler(commands=['view-progress'])
def view_progress(message):
    user_ref = db.reference('users/'+ str(message.chat.id) + '/plan')
    plan = user_ref.get()
    curr_ref = db.reference('plan-progress/' + str(message.chat.id) + "/" + plan)
    data = curr_ref.get()
    tasklist = data['plan-progress']
    bot.send_message(message.chat.id, tasklist)

@bot.message_handler(commands=['mark-task'])
def mark_task(message):
    task_no = message.text.split(" ")[1]
    curr_ref = db.reference('plan-progress/' + str(message.chat.id) + "/plan-progress")

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "Help Message")

# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")

bot.polling()

#     Done! Congratulations on your new bot. You will find it at t.me/learningbuddies_bot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.

# Use this token to access the HTTP API:
# 6233481401:AAHrhtvZ9ivUdCS-jjiq2f6IeSusyg7ZKPI
# Keep your token secure and store it safely, it can be used by anyone to control your bot.

# For a description of the Bot API, see this page: https://core.telegram.org/bots/api

