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
queue = []

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
    user_ref = db.reference('users/'+ str(message.chat.id))
    user = user_ref.get()
    print(user['partnerid'])
    if user['partnerid'] != 'None':
        bot.reply_to(message, "Sorry! You're already matched.")
        return
    plan = user['plan']
    queue_ref = db.reference('queue')
    queue = queue_ref.get()
    if queue != None:
        if str(message.chat.id) in list(queue.keys()):
            bot.send_message(message.chat.id, "You're still being matched! Hold on...")
            return
        eligible_users = list(filter(lambda x: x['plan'] == plan, queue.values()))
    if queue and eligible_users:
        partner = eligible_users.pop(0)
        user['partnerid'] = partner['id']
        user_ref.set(user)
        partner_ref = db.reference('users/' + partner['id'])
        partner_obj = partner_ref.get()
        partner_obj['partnerid'] = str(message.chat.id)
        partner_ref.set(partner_obj)

        #delete from db queue
        delete_ref = db.reference("queue/" + partner["id"])
        delete_ref.delete()
        
        thisuser = message.from_user.username
        bot.send_message(message.chat.id, "You've been matched with @" + partner['username'] + "!")
        bot.send_message(partner['id'], "You've been matched with @" + thisuser + "!")
        return
    teleuser = message.from_user.username
    if queue == None:
        queue = []
    else:
        queue = list(queue.values())
    queue.append({'id': str(message.chat.id), 'plan': plan, 'username': teleuser})
    res_dct = {queue[i]['id']: queue[i] for i in range(0, len(queue), 2)}
    queue_ref.set(res_dct)
    bot.reply_to(message, "I'll notify you once we find you a match. Starting the matching process...")


@bot.message_handler(commands=['select-plan'])
def plan_selector(message):
    plan_code = message.text.split(" ")[1]
    if plan_code in plan_codes:
        curr_ref = db.reference('users/'+str(message.chat.id)+'/plan')
        curr_ref.set(plan_code)
        plan_ref = db.reference('plan-progress/' + str(message.chat.id) + "/" + plan_code)
        plan_ref.set({'plan-progress': PlanProgress.getprogress(), 'currtask': 0, 'iscomplete' : False})

        # remove user from queue if they are in it
        queue_ref = db.reference("queue/" + str(message.chat.id))
        queue_ref.delete()

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
    #TASK: format tasklist
    tlstring = "Your progress: \n"
    for idx, task in enumerate(tasklist):
        emoji = " ❌"
        if int(task[0]) == 1:
            emoji = " ✅"
        tlstring += str(idx) + ". " + task[1].strip("\n") +  emoji + "\n"
    bot.send_message(message.chat.id, tlstring)

@bot.message_handler(commands=['view-partner-progress'])
def view_partner_progress(message):
    user_ref = db.reference('users/'+ str(message.chat.id))
    user = user_ref.get()
    partner_id = user["partnerid"]
    if partner_id == "None":
        bot.send_message(message.chat.id, "You don't have a partner yet! Try /match to find one.")
        return
    plan = user["plan"]
    curr_ref = db.reference('plan-progress/' + partner_id + "/" + plan)
    data = curr_ref.get()
    tasklist = data['plan-progress']
    #TASK: format tasklist
    tlstring = "Your partner's progress: \n"
    for idx, task in enumerate(tasklist):
        emoji = " ❌"
        if int(task[0]) == 1:
            emoji = " ✅"
        tlstring += str(idx) + ". " + task[1].strip("\n") +  emoji + "\n"
    bot.send_message(message.chat.id, tlstring)

@bot.message_handler(commands=['mark-task'])
def mark_task(message):
    plan_ref = db.reference('users/'+ str(message.chat.id) + '/plan')
    plan = plan_ref.get()
    current_task_ref = db.reference('plan-progress/'+ str(message.chat.id) + '/' + plan + '/currtask')
    current_task = current_task_ref.get()
    task_no = int(message.text.split(" ")[1])
    if task_no <= current_task and (task_no == 0 or haspartnerfinishedprev(message.chat.id)):
        curr_ref = db.reference('plan-progress/' + str(message.chat.id) + "/" + plan + "/plan-progress")
        tasklist = curr_ref.get()
        tasklist[task_no][0] = '1 '
        curr_ref.set(tasklist)
        if task_no == current_task:
            current_task_ref.set(task_no + 1)
        bot.reply_to(message, "I have marked this task as completed! Task: " + tasklist[task_no][1])
    else:
        bot.reply_to(message, "I'm sorry. I cannot mark this task. You have not done the previous tasks yet!")

def haspartnerfinishedprev(user_id):
    user_ref = db.reference('users/'+ str(user_id))
    user = user_ref.get()
    partner_id = user["partnerid"]
    if partner_id == "None":
        return True
    user_ct_ref = db.reference('plan-progress/'+str(user_id)+"/"+user["plan"]+"/currtask")
    partner_ct_ref = db.reference('plan-progress/'+str(partner_id)+"/"+user["plan"]+"/currtask")
    user_ct = user_ct_ref.get()
    partner_ct = partner_ct_ref.get()
    if partner_ct + 1 == user_ct:
        return True
    bot.send_message(user_id, "Oh no! You're partner is lagging behind. You can only proceed after he catched up! Motivate them.")
    bot.send_message(partner_id, "Your partner is ready to move on! Better catch up soon...")
    return False

@bot.message_handler(commands=["view-curr-task"])
def view_curr_task(message):
    plan_ref = db.reference('users/'+ str(message.chat.id) + '/plan')
    plan = plan_ref.get()
    current_task_ref = db.reference('plan-progress/'+ str(message.chat.id) + '/' + plan + '/currtask')
    current_task = current_task_ref.get()
    curr_ref = db.reference('plan-progress/' + str(message.chat.id) + "/" + plan + "/plan-progress")
    tasklist = curr_ref.get()
    bot.reply_to(message, "Your current task: " + tasklist[current_task][1])

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

