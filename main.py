import telebot
from telebot import types
from database import get_demo
from controllers import main_menu, handle_homework, handle_schedule
from models import get_subjects


def handle_add(bot, message):
    try:
        subjects = get_subjects()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for subject in subjects:
            keyboard.add(types.KeyboardButton(subject))
        bot.send_message(message.chat.id, "Выберите предмет:", reply_markup=keyboard)
        bot.register_next_step_handler(message, process_subject, bot)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при добавлении: {e}')


def process_subject(message, bot):
    try:
        subject = message.text.strip()
        if subject not in get_subjects():
            bot.send_message(message.chat.id, "Некорректный предмет. Попробуйте снова.", reply_markup=main_menu())
            return
        bot.send_message(message.chat.id, "Введите задание:", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, process_task, bot, subject)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при вводе предмета: {e}')


def process_task(message, bot, subject):
    try:
        task = message.text.strip()
        from database import save_homework
        save_homework(subject, task)
        bot.send_message(message.chat.id, f'Задание по {subject} добавлено!', reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при сохранении задания: {e}')


TOKEN = '7621511398:AAFNKXjit_zuUPkUdYaZYqFHu2mRg2NpebU'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        bot.send_message(message.chat.id, 'Привет! Я бот для школьников!', reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при запуске: {e}')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        text = message.text.strip()
        if not text:
            bot.send_message(message.chat.id, 'Введите сообщение!', reply_markup=main_menu())
            return

        commands = {
            '📚 Д/З 📚': handle_homework,
            '✍ Демо ✍': get_demo,
            '🕒 Расписание 🕒': handle_schedule,
            '➕ Добавить ➕': handle_add
        }

        if text in commands:
            bot.register_next_step_handler(message, lambda msg: commands[text](bot, msg))
        else:
            bot.send_message(message.chat.id, 'Не понимаю команду. Используйте кнопки.', reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}')


if __name__ == "__main__":
    print("Бот запущен...")
    while True:
        try:
            bot.polling(non_stop=True, interval=1)
        except Exception:
            pass
