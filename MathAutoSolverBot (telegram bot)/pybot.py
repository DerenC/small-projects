import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import math
import cmath

from config import *

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Command handlers
def start(update: Update, _: CallbackContext) -> None:
  user = update.effective_user
  update.message.reply_text(f'Greetings, {user.first_name} {user.last_name if user.last_name else ""}')

def help_command(update: Update, _: CallbackContext) -> None:
  update.message.reply_text('Help!')
  
def isFloat(num):
  try:
    float(num)
    return True
  except ValueError:
    return False

def isInt(num):
  try:
    int(num)
    return True
  except ValueError:
    return False

def isNum(num):
  return isInt(num) or isFloat(num)

def convStr(num, post) -> str:
  conv = lambda x: abs(x)/x if x else 0 
  switcher = ["x\u00b2", 'x', '']
  if num:
    if num == 1:
      if post == 0:
        return switcher[post]
      if post == 2:
        return "+1" 
      return "+" + switcher[post]
    if num == -1:
      if post == 2:
        return "-1"
      return "-" + switcher[post]
    if num > 1:
      if post == 0:
        return f"{num}" + switcher[post]
      return f"+{num}" + switcher[post]
    if num < -1:
      return f"{num}" + switcher[post]
  return ''

def solveQuadratic(update: Update, _: CallbackContext) -> None:
  splitted_message = update.message.text.split()
  if len(splitted_message) == 4 and isNum(splitted_message[1]) and isNum(splitted_message[2]) and isNum(splitted_message[3]):
    a, b, c = map(int, splitted_message[1:])
    eqt = convStr(a,0) + convStr(b,1) + convStr(c,2)
    try:
      dism = math.sqrt(b**2 - 4*a*c)
    except ValueError: 
      dism = cmath.sqrt(b**2 - 4*a*c)
    sol1, sol2 = ((-1) * b + dism) / (2*a), ((-1) * b - dism) / (2*a)
    if sol1 == sol2:
      update.message.reply_text(f'The soluton to {eqt} is {sol1}.')
    else:
      update.message.reply_text(f'The solutons to {eqt} are {sol1} and {sol2}.')
  else:
    update.message.reply_text('Please key in 3 numbers.')

def echo(update: Update, _: CallbackContext) -> None:
  update.message.reply_text(f"you said {update.message.text}")

def main() -> None:
  updater = Updater(TOKEN)

  dispatcher = updater.dispatcher

  dispatcher.add_handler(CommandHandler("start", start))
  dispatcher.add_handler(CommandHandler("help", help_command))
  dispatcher.add_handler(CommandHandler("solveQuadratic", solveQuadratic))

  dispatcher.add_handler(MessageHandler(Filters.text, echo))

  # Polling means the server will keep checking for any incoming message, with the chatbot
  # Another approach is to use a webhook
  updater.start_polling()

  updater.idle()

if __name__ == "__main__":
  main()