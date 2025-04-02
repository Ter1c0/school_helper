import telebot
from telebot import types
from controllers import handle_homework, handle_demo, handle_schedule, main_menu
from models import get_subjects, get_days, get_content_types
from database import save_homework, save_demo, save_schedule

import os

bot = telebot.TeleBot(os.getenv("TG_TOKEN"))

def create_keyboard(items):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for item in items:
        keyboard.add(types.KeyboardButton(item))
    return keyboard

def handle_add(bot, message):
    keyboard = create_keyboard(get_content_types())
    msg = bot.send_message(message.chat.id, "Что вы хотите добавить?", reply_markup=keyboard)
    bot.register_next_step_handler(msg, select_subject_or_day, bot)

def select_subject_or_day(message, bot):
    content_type = message.text.strip()
    if content_type == "Расписание":
        keyboard = create_keyboard(get_days())
        msg = bot.send_message(message.chat.id, "Выберите день:", reply_markup=keyboard)
        bot.register_next_step_handler(msg, lambda m: handle_schedule_day(m, bot))
    else:
        keyboard = create_keyboard(get_subjects())
        msg = bot.send_message(message.chat.id, f"Выберите предмет для {content_type}:", reply_markup=keyboard)
        bot.register_next_step_handler(msg, lambda m: handle_subject(m, bot, content_type))

def handle_subject(message, bot, content_type):
    subject = message.text.strip()
    if subject in get_subjects():
        msg = bot.send_message(message.chat.id, "Введите задание:", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, lambda m: save_task(m, bot, subject, content_type))
    else:
        bot.send_message(message.chat.id, "Неверный предмет", reply_markup=main_menu())

def handle_schedule_day(message, bot):
    day = message.text.strip()
    if day in get_days():
        keyboard = create_keyboard(get_subjects())
        msg = bot.send_message(message.chat.id, "Выберите предмет:", reply_markup=keyboard)
        bot.register_next_step_handler(msg, lambda m: handle_schedule_subject(m, bot, day))
    else:
        bot.send_message(message.chat.id, "Неверный день", reply_markup=main_menu())

def handle_schedule_subject(message, bot, day):
    subject = message.text.strip()
    if subject in get_subjects():
        msg = bot.send_message(message.chat.id, "Введите время (например, 9:00-9:45):", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, lambda m: save_schedule_time(m, bot, day, subject))
    else:
        bot.send_message(message.chat.id, "Неверный предмет", reply_markup=main_menu())

def save_task(message, bot, subject, content_type):
    task = message.text.strip()
    try:
        if content_type == "ДЗ":
            msg = bot.send_message(message.chat.id, 
                                 "Введите дату сдачи (формат ДД.ММ):", 
                                 reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(msg, save_homework_with_date, 
                                         bot, subject, task)
        elif content_type == "Демо":
            msg = bot.send_message(message.chat.id,
                                 "Введите дату модульной работы (формат ДД.ММ):",
                                 reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(msg, lambda m: save_demo_with_date(m, bot, subject, task))
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}", 
                        reply_markup=main_menu())

def save_homework_with_date(message, bot, subject, task):
    try:
        due_date = message.text.strip()
        if len(due_date.split('.')) != 2:
            raise ValueError("Неверный формат даты")
            
        day, month = map(int, due_date.split('.'))
        if not (1 <= day <= 31 and 1 <= month <= 12):
            raise ValueError("Неверная дата")
            
        save_homework(subject, task, due_date)
        bot.send_message(message.chat.id, 
                        f"Задание по {subject} добавлено!\n"
                        f"Срок сдачи: {due_date}", 
                        reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, 
                        "Ошибка! Введите дату в формате ДД.ММ", 
                        reply_markup=main_menu())

def save_schedule_time(message, bot, day, subject):
    time = message.text.strip()
    try:
        save_schedule(day, subject, time)
        bot.send_message(message.chat.id, f"Расписание для {subject} в {day} добавлено!", reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}", reply_markup=main_menu())

def save_demo_with_date(message, bot, subject, task):
    try:
        due_date = message.text.strip()
        if len(due_date.split('.')) != 2:
            raise ValueError("Неверный формат даты")
            
        day, month = map(int, due_date.split('.'))
        if not (1 <= day <= 31 and 1 <= month <= 12):
            raise ValueError("Неверная дата")
            
        task_with_date = f"{task} (Модульная: {due_date})"
        save_demo(subject, task_with_date)
        bot.send_message(message.chat.id, 
                        f"Демо задание по {subject} добавлено!\n"
                        f"Дата модульной: {due_date}", 
                        reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, 
                        "Ошибка! Введите дату в формате ДД.ММ", 
                        reply_markup=main_menu())

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот для школьников!', reply_markup=main_menu())

@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text.strip()
    if text == '📚 Д/З 📚':
        handle_homework(bot, message)
    elif text == '✍ Демо ✍':
        handle_demo(bot, message)
    elif text == '🕒 Расписание 🕒':
        handle_schedule(bot, message)
    elif text == '➕ Добавить ➕':
        handle_add(bot, message)
    else:
        bot.send_message(message.chat.id, 'Используйте кнопки меню', reply_markup=main_menu())

if __name__ == "__main__":
    print("Бот запущен...")
    while True:
        try:
            bot.polling(non_stop=True, interval=1)
        except Exception as e:
            print(f"Ошибка: {e}")
            continue
