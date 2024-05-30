import telebot
# Введите сюда токен бота, пример 11111111:AAAAAAAAAAAA
API_TOKEN = '___'
bot = telebot.TeleBot(API_TOKEN)
# Введите сюда канал username, пример @Example
CHANNEL_ID = '___'

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
