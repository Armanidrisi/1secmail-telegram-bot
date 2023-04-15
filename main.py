import telebot
import requests
import datetime
from Config import DATABASE_URI,TOKEN,BASE_URL
from Database import UserDatabase


#Create a bot instance
bot = telebot.TeleBot(TOKEN)
#create a database instance
db = UserDatabase(DATABASE_URI)

@bot.message_handler(commands=["start"])
def send_text(message):
  if db.get_num_rows_by_id(message.chat.id) == 0:
    db.create_user(message.chat.first_name, message.chat.last_name, message.chat.id, None)
  keyboard = telebot.types.ReplyKeyboardMarkup(True)
  keyboard.row("🚀 My Email")
  keyboard.row("📨 Inbox","📧 Generate New Email")
  keyboard.row("📊  Status")
  msg=f"*Hello {message.chat.first_name}*\n\n_I am simple Temporary Email Bot\nI can Generate Temporary Emails For You_"
  bot.reply_to(message,msg,parse_mode ="Markdown",reply_markup=keyboard)

@bot.message_handler(content_types=["text"])
def send_msg(message):
  if message.text=="🚀 My Email":
    u = db.get_user(message.chat.id)
    #print(u.email,u.first_name)
    if u.email:
      bot.send_message(message.chat.id,f"*🚀 Your Temporary Email Is\n\n{u.email}*",parse_mode="Markdown")
    else:
      bot.send_message(message.chat.id,"_❌️ No Email Found_", parse_mode="Markdown")
  elif message.text == "📧 Generate New Email":
    r = requests.get(f"{BASE_URL}?action=genRandomMailbox")
    email = r.json()[0]
    m = f"Your Email Successfully Generated :\n\n{email}"
    db.update_user(message.chat.id,{'email':email})
    bot.send_message(message.chat.id,m)
  elif message.text == "📨 Inbox":
    u = db.get_user(message.chat.id)
    #print(u.email,u.first_name)
    if u.email:
      em = u.email
      uname=em[:em.index("@")]
      domain=em[em.index("@") + 1:]
      r = requests.get(f"{BASE_URL}?action=getMessages&login={uname}&domain={domain}")
      print(r.json())
      msg_inbox = "*🟢 Received Emails\n\n"
      if r.json() != []:
        for c in r.json():
          msg_inbox += f"\nFrom: {c['from']}\nTo: {em}\nSubject: {c['subject']}\nDate: {c['date']}\nMessage ID: {c['id']}\n\n➖➖➖➖➖➖➖➖➖➖➖\n\n"
        msg_inbox += "Send Message ID To See The Message\n*"
        bot.send_message(message.chat.id,msg_inbox,parse_mode ="Markdown")
        bot.register_next_step_handler(message, get_message)
      else:
        bot.send_message(message.chat.id,"_❌️ No Message Found_",parse_mode="Markdown")
    else:
      bot.send_message(message.chat.id,"_❌️ No Email Found_", parse_mode="Markdown")
  if message.text == "📊  Status":
    u=db.get_num_rows()
    current_time = datetime.datetime.now()
    current_date = datetime.date.today()
    t = current_time.strftime("%H:%M:%S")
    d = current_date.strftime("%d/%m/%Y")
    m = f"*📊 Bot Live Statistics\n\n⚡ Total Users: {u}\n\n🔝 Data for: (Today)\n📅 Date: 15/4/2023\n🕐 Time: 6:36:28 AM*"
    bot.send_message(message.chat.id,m,parse_mode ="Markdown")
  
def get_message(message):
  u = db.get_user(message.chat.id)
    #print(u.email,u.first_name)
  if u.email:
    em = u.email
    uname=em[:em.index("@")]
    domain=em[em.index("@") + 1:]
    
    r = requests.get(f"{BASE_URL}?action=readMessage&login={uname}&domain={domain}&id={message.text}")
    j = r.json()
    m = f"*👉 From: {j['from']}\n\n👉 Subject: {j['subject']}\n\n👉 Message: {j['textBody']}*"
    bot.send_message(message.chat.id,m,parse_mode="Markdown")
    
if __name__ == '__main__':
  bot.polling(none_stop =True )