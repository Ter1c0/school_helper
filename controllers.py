# === controllers.py ===
from database import get_homework, get_demo

from telebot import types
from models import get_subjects, get_content_types

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

def process_demo_subject(message, bot):
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
    try:
        from models import get_days
        days = get_days()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for day in days:
            keyboard.add(types.KeyboardButton(day))
        bot.send_message(message.chat.id, "Выберите день недели для просмотра расписания:", reply_markup=keyboard)
        bot.register_next_step_handler(message, process_schedule_view, bot)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')

def process_schedule_view(message, bot):
    try:
        day = message.text.strip()
        if day not in get_days():
            bot.send_message(message.chat.id, "Некорректный день. Попробуйте снова.", reply_markup=main_menu())
            return
        from database import get_schedule
        schedules = get_schedule(day)
        reply = f"🕒 Расписание на {day}:\n" + ("\n".join([s[0] for s in schedules]) if schedules else "Расписание не найдено!")
        bot.send_message(message.chat.id, reply, reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')

def handle_add(bot, message):
    try:
        content_types = get_content_types()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for content_type in content_types:
            keyboard.add(types.KeyboardButton(content_type))
        bot.send_message(message.chat.id, "Выберите тип контента:", reply_markup=keyboard)
        bot.register_next_step_handler(message, process_content_type, bot)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')


def process_content_type(message, bot):
    try:
        content_type = message.text.strip()
        bot.send_message(message.chat.id, f"Вы выбрали тип контента: {content_type}.  Дальнейшая реализация добавления контента будет добавлена позже.")
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')
