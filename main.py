import telebot
from telebot import types

from controllers import handle_homework, handle_schedule, handle_demo, main_menu
from models import get_subjects


def handle_add(bot, message):
    try:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton("ДЗ"), types.KeyboardButton("Демо"),
                     types.KeyboardButton("Расписание"))
        keyboard.add(types.KeyboardButton("Отмена"))
        bot.send_message(message.chat.id,
                         "Что вы хотите добавить?",
                         reply_markup=keyboard)
        bot.register_next_step_handler(message, process_content_type, bot)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при добавлении: {e}')


def process_content_type(message, bot):
    try:
        content_type = message.text.strip()
        if content_type == "Отмена":
            bot.send_message(message.chat.id,
                             "Добавление отменено",
                             reply_markup=main_menu())
            return

        if content_type not in ["ДЗ", "Демо", "Расписание"]:
            bot.send_message(
                message.chat.id,
                "Некорректный тип. Выберите ДЗ, Демо или Расписание",
                reply_markup=main_menu())
            return

        if content_type == "Расписание":
            from models import get_days
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for day in get_days():
                keyboard.add(types.KeyboardButton(day))
            bot.send_message(message.chat.id,
                             "Выберите день недели:",
                             reply_markup=keyboard)
            bot.register_next_step_handler(message, process_schedule_day, bot)
        else:
            subjects = get_subjects()
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for subject in subjects:
                keyboard.add(types.KeyboardButton(subject))
            bot.send_message(message.chat.id,
                             f"Выберите предмет для {content_type}:",
                             reply_markup=keyboard)
            bot.register_next_step_handler(message, process_subject, bot,
                                           content_type)
    except Exception as e:
        bot.send_message(message.chat.id,
                         f'Ошибка при выборе типа контента: {e}')


def process_subject(message, bot, content_type):
    try:
        subject = message.text.strip()
        if subject not in get_subjects():
            bot.send_message(message.chat.id,
                             "Некорректный предмет. Попробуйте снова.",
                             reply_markup=main_menu())
            return

        if content_type == "ДЗ":
            msg_text = "Введите домашнее задание:"
        elif content_type == "Демо":
            msg_text = "Введите демо-задание:"
        else:
            msg_text = "Что-то пошло не так"

        bot.send_message(message.chat.id,
                         msg_text,
                         reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, process_task, bot, subject,
                                       content_type)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при вводе предмета: {e}')


def process_task(message, bot, subject, content_type):
    try:
        task = message.text.strip()
        success_msg = ""

        if content_type == "ДЗ":
            from database import save_homework
            save_homework(subject, task)
            success_msg = f'Домашнее задание по {subject} добавлено!'
        elif content_type == "Демо":
            from database import save_demo
            save_demo(subject, task)
            success_msg = f'Демо-задание по {subject} добавлено!'
        else:
            success_msg = f'Задание типа {content_type} по {subject} добавлено!'

        bot.send_message(message.chat.id,
                         success_msg,
                         reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id,
                         f'Ошибка при сохранении задания: {e}')


def process_schedule_day(message, bot):
    try:
        day = message.text.strip()
        from models import get_days
        if day not in get_days():
            bot.send_message(message.chat.id,
                             "Некорректный день недели. Попробуйте снова.",
                             reply_markup=main_menu())
            return

        subjects = get_subjects()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for subject in subjects:
            keyboard.add(types.KeyboardButton(subject))
        bot.send_message(message.chat.id,
                         f"Выберите предмет для расписания в {day}:",
                         reply_markup=keyboard)
        bot.register_next_step_handler(message, process_schedule_subject, bot,
                                       day)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при выборе дня недели: {e}')


def process_schedule_subject(message, bot, day):
    try:
        subject = message.text.strip()
        if subject not in get_subjects():
            bot.send_message(message.chat.id,
                             "Некорректный предмет. Попробуйте снова.",
                             reply_markup=main_menu())
            return

        bot.send_message(message.chat.id,
                         "Введите время урока (например, 9:00-9:45):",
                         reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, process_schedule_time, bot,
                                       day, subject)
    except Exception as e:
        bot.send_message(message.chat.id,
                         f'Ошибка при выборе предмета для расписания: {e}')


def process_schedule_time(message, bot, day, subject):
    try:
        time = message.text.strip()
        from database import save_schedule
        save_schedule(day, subject, time)
        bot.send_message(
            message.chat.id,
            f'Расписание для {subject} в {day} ({time}) добавлено!',
            reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id,
                         f'Ошибка при сохранении расписания: {e}')


def select_subject_for_homework(message, bot):
    try:
        subjects = get_subjects()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for subject in subjects:
            keyboard.add(types.KeyboardButton(subject))
        bot.send_message(message.chat.id,
                         "Выберите предмет для добавления Д/З:",
                         reply_markup=keyboard)
        bot.register_next_step_handler(message, process_homework_subject_add,
                                       bot)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при выборе предмета: {e}')


def select_subject_for_demo(message, bot):
    try:
        subjects = get_subjects()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for subject in subjects:
            keyboard.add(types.KeyboardButton(subject))
        bot.send_message(message.chat.id,
                         "Выберите предмет для добавления Демо:",
                         reply_markup=keyboard)
        bot.register_next_step_handler(message, process_demo_subject_add, bot)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при выборе предмета: {e}')


def process_demo_subject_add(message, bot):
    try:
        subject = message.text.strip()
        if subject not in get_subjects():
            bot.send_message(message.chat.id,
                             "Некорректный предмет. Попробуйте снова.",
                             reply_markup=main_menu())
            return
        bot.send_message(message.chat.id,
                         "Введите демо-задание:",
                         reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, process_demo_task, bot,
                                       subject)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при вводе предмета: {e}')


def process_demo_task(message, bot, subject):
    try:
        task = message.text.strip()
        from database import save_demo
        save_demo(subject, task)
        bot.send_message(message.chat.id,
                         f'Демо-задание по {subject} добавлено!',
                         reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id,
                         f'Ошибка при сохранении задания: {e}')


def add_schedule(message, bot):
    try:
        from models import get_days
        days = get_days()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for day in days:
            keyboard.add(types.KeyboardButton(day))
        bot.send_message(message.chat.id,
                         "Выберите день недели:",
                         reply_markup=keyboard)
        bot.register_next_step_handler(message, process_schedule_day, bot)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при выборе дня: {e}')


def process_homework_subject_add(message, bot):
    try:
        subject = message.text.strip()
        if subject not in get_subjects():
            bot.send_message(message.chat.id,
                             "Некорректный предмет. Попробуйте снова.",
                             reply_markup=main_menu())
            return
        bot.send_message(message.chat.id,
                         "Введите задание:",
                         reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, process_task, bot, subject,
                                       "ДЗ")
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при вводе предмета: {e}')


TOKEN = '7621511398:AAFNKXjit_zuUPkUdYaZYqFHu2mRg2NpebU'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        bot.send_message(message.chat.id,
                         'Привет! Я бот для школьников!',
                         reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при запуске: {e}')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        text = message.text.strip()
        if not text:
            bot.send_message(message.chat.id,
                             'Введите сообщение!',
                             reply_markup=main_menu())
            return

        if text == '📚 Д/З 📚':
            handle_homework(bot, message)
        elif text == '✍ Демо ✍':
            handle_demo(bot, message)
        elif text == '🕒 Расписание 🕒':
            handle_schedule(bot, message)
        elif text == '➕ Добавить ➕':
            handle_add(bot, message)
        else:
            bot.send_message(message.chat.id,
                             'Не понимаю команду. Используйте кнопки.',
                             reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}')


if __name__ == "__main__":
    print("Бот запущен...")
    while True:
        try:
            bot.polling(non_stop=True, interval=1)
        except Exception:
            pass
