# === controllers.py ===
from database import get_homework, get_demo

from telebot import types
from models import get_subjects

def handle_homework(bot, message):
    try:
        subjects = get_subjects()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for subject in subjects:
            keyboard.add(types.KeyboardButton(subject))
        bot.send_message(message.chat.id, "Выберите предмет для просмотра Д/З:", reply_markup=keyboard)
        bot.register_next_step_handler(message, process_homework_subject, bot)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')

def process_homework_subject(message, bot):
    try:
        subject = message.text.strip()
        if subject not in get_subjects():
            bot.send_message(message.chat.id, "Некорректный предмет. Попробуйте снова.", reply_markup=main_menu())
            return
        tasks = get_homework(subject)
        reply = f"📚 Д/З по {subject}:\n" + ("\n".join([t[0] for t in tasks]) if tasks else "Заданий нет! Вы молодцы! 🎉")
        bot.send_message(message.chat.id, reply, reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')

def handle_demo(bot, message):
    try:
        subjects = get_subjects()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for subject in subjects:
            keyboard.add(types.KeyboardButton(subject))
        bot.send_message(message.chat.id, "Выберите предмет для просмотра демо:", reply_markup=keyboard)
        bot.register_next_step_handler(message, process_demo_subject, bot)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')

def process_demo_subject(bot, message):
    try:
        subject = message.text.strip()
        if subject not in get_subjects():
            bot.send_message(message.chat.id, "Некорректный предмет. Попробуйте снова.", reply_markup=main_menu())
            return
        demos = get_demo(subject)
        reply = f"✍ Демо по {subject}:\n" + ("\n".join([t[0] for t in demos]) if demos else "Нет доступных демо-заданий!")
        bot.send_message(message.chat.id, reply, reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')

def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('📚 Д/З 📚', '🕒 Расписание 🕒')
    keyboard.add('✍ Демо ✍', '➕ Добавить ➕')
    return keyboard

def handle_schedule(bot, message):
    bot.send_message(message.chat.id, "Функция расписания пока не реализована.", reply_markup=main_menu())
