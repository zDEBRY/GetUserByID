import os
import configparser
import telebot

CONFIG_FILE = 'config.ini'
config = configparser.ConfigParser()

if not os.path.exists(CONFIG_FILE):
    API_TOKEN = input("Введите токен бота: (API_TOKEN): ")
    CHANNEL_ID = input("Введите ID канала со знаком @: (CHANNEL_ID): ")
    config['settings'] = {
        'API_TOKEN': API_TOKEN,
        'CHANNEL_ID': CHANNEL_ID
    }
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
else:
    config.read(CONFIG_FILE)
    API_TOKEN = config['settings']['API_TOKEN']
    CHANNEL_ID = config['settings']['CHANNEL_ID']

if not API_TOKEN or not CHANNEL_ID:
    raise ValueError("API_TOKEN и CHANNEL_ID должны быть установлены.")

bot = telebot.TeleBot(API_TOKEN)

def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'creator']
    except Exception as e:
        print(f"Ошибка при проверке подписки: {e}")
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if is_subscribed(message.from_user.id):
        bot.reply_to(message, "Привет! Отправь мне ID пользователя, и я дам тебе ссылку на его профиль.")
    else:
        sent_message = bot.send_message(message.chat.id, f"Подпишитесь на канал {CHANNEL_ID}, чтобы пользоваться ботом.")
        bot.register_next_step_handler(sent_message, delete_message)

def delete_message(message):
    bot.delete_message(message.chat.id, message.message_id)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if is_subscribed(message.from_user.id):
        user_id = message.text
        try:
            int(user_id)
            user_link = (
                f"<b>tg://user?id={user_id} - ПК/IOS/Android</b>\n"
                f"<b>https://t.me/@id{user_id} - IOS</b>\n"
                f"<b>tg://openmessage?user_id={user_id} - Android</b>"
            )
            bot.reply_to(message, f"<i>Ссылки на пользователя для каждого устройства:</i>\n{user_link}\n<i>(Учтите, что доступ к профилю может быть ограничен)</i>", parse_mode='HTML')
        except ValueError:
            bot.reply_to(message, 'Пожалуйста, введите правильный числовой ID пользователя.')
    else:
        bot.reply_to(message, f"Подпишитесь на канал {CHANNEL_ID}, чтобы пользоваться ботом.")

bot.polling()
