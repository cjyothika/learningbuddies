# learningbuddies

LearningBuddies is a telegram bot that matches you with a likeminded individual to keep you accountable for your progress towards your goals. 
Pick a plan and get matched with a partner. Chat with your partner and get each other motivated. Tick off tasks but you can only tick off the next
task after your partner has finished their current task. You no longer have to learn skills in isolation! Having someone on the same journey as
you can be rewarding.

## /start
Starts the telegram bot and registers you as a user.

## /select-plan {plan-code} or /selectplan {plan-code}
Eg. /select-plan learn-angular will load an angular study plan for you.
Available plan-codes: learn-angular, learn-react, 75-hard, couch25k

## /match
Get matched with a partner on the same journey as you!

## /view-progress or /viewprogress
View the progress you have made on your study plan

## /view-partner-progress or /viewpartnerprogress
View your partner's progress

## /mark-task {task-number} or /marktask {task-number}
Mark your task according to the index shown by the /view-progress command as completed. You can only be ahead of your partner by at most 1 task.
Eg. /mark-task 0

## /view-curr-task
View your current task
