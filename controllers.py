
from telebot import types
from database import get_homework, get_demo, get_schedule
from models import get_subjects, get_days

def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton("📚 Д/З 📚"),
        types.KeyboardButton("✍ Демо ✍")
    )
    keyboard.add(
        types.KeyboardButton("🕒 Расписание 🕒"),
        types.KeyboardButton("➕ Добавить ➕")
    )
    return keyboard

def homework_view_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("📚 Все задания 📚"))
    keyboard.add(types.KeyboardButton("📖 Выбрать предмет 📖"))
    keyboard.add(types.KeyboardButton("🔙 Назад"))
    return keyboard

def format_homework(homework):
    if not homework:
        return "Нет домашних заданий"
    formatted = "📚 Домашние задания:\n\n"
    for subj, task, due_date in homework:
        formatted += f"📌 {subj}\n📝 {task}\n📅 Сдать до: {due_date}\n\n"
    return formatted

def handle_homework(bot, message):
    bot.send_message(message.chat.id, "Выберите опцию:", 
                    reply_markup=homework_view_menu())
    bot.register_next_step_handler(message, process_homework_choice, bot)

def process_homework_choice(message, bot):
    text = message.text.strip()
    if text == "📚 Все задания 📚":
        homework = get_homework()
        bot.send_message(message.chat.id, format_homework(homework), 
                        reply_markup=main_menu())
    elif text == "📖 Выбрать предмет 📖":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for subject in get_subjects():
            keyboard.add(types.KeyboardButton(subject))
        keyboard.add(types.KeyboardButton("🔙 Назад"))
        bot.send_message(message.chat.id, "Выберите предмет:", 
                        reply_markup=keyboard)
        bot.register_next_step_handler(message, show_subject_homework, bot)
    elif text == "🔙 Назад":
        bot.send_message(message.chat.id, "Главное меню:", 
                        reply_markup=main_menu())

def show_subject_homework(message, bot):
    subject = message.text.strip()
    if subject == "🔙 Назад":
        bot.send_message(message.chat.id, "Главное меню:", 
                        reply_markup=main_menu())
        return
    homework = get_homework(subject)
    bot.send_message(message.chat.id, format_homework(homework), 
                    reply_markup=main_menu())

def demo_view_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("📚 Все демо версии 📚"))
    keyboard.add(types.KeyboardButton("📖 Выбрать предмет 📖"))
    keyboard.add(types.KeyboardButton("🔙 Назад"))
    return keyboard

def handle_demo(bot, message):
    bot.send_message(message.chat.id, "Выберите опцию:", 
                    reply_markup=demo_view_menu())
    bot.register_next_step_handler(message, process_demo_choice, bot)

def process_demo_choice(message, bot):
    text = message.text.strip()
    if text == "📚 Все демо версии 📚":
        demos = get_demo()
        text = "✍ Демо задания:\n\n" + "\n".join(f"{subj}: {task}" 
                                                for subj, task in demos)
        bot.send_message(message.chat.id, text or "Нет демо заданий", 
                        reply_markup=main_menu())
    elif text == "📖 Выбрать предмет 📖":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for subject in get_subjects():
            keyboard.add(types.KeyboardButton(subject))
        keyboard.add(types.KeyboardButton("🔙 Назад"))
        bot.send_message(message.chat.id, "Выберите предмет:", 
                        reply_markup=keyboard)
        bot.register_next_step_handler(message, show_subject_demo, bot)
    elif text == "🔙 Назад":
        bot.send_message(message.chat.id, "Главное меню:", 
                        reply_markup=main_menu())

def show_subject_demo(message, bot):
    subject = message.text.strip()
    if subject == "🔙 Назад":
        bot.send_message(message.chat.id, "Главное меню:", 
                        reply_markup=main_menu())
        return
    demos = [demo for demo in get_demo() if demo[0] == subject]
    text = f"✍ Демо задания по {subject}:\n\n" + "\n".join(f"{task}" 
                                                          for _, task in demos)
    bot.send_message(message.chat.id, text or f"Нет демо заданий по {subject}", 
                    reply_markup=main_menu())

def handle_schedule(bot, message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for day in get_days():
        keyboard.add(types.KeyboardButton(day))
    keyboard.add(types.KeyboardButton("📅 Все дни"))
    keyboard.add(types.KeyboardButton("🔙 Назад"))
    bot.send_message(message.chat.id, "Выберите день недели:", 
                    reply_markup=keyboard)
    bot.register_next_step_handler(message, show_schedule, bot)

def show_schedule(message, bot):
    text = message.text.strip()
    if text == "🔙 Назад":
        bot.send_message(message.chat.id, "Главное меню:", 
                        reply_markup=main_menu())
        return
    
    schedule = get_schedule()
    if text == "📅 Все дни":
        text = "🕒 Расписание:\n\n" + "\n".join(f"{day} - {subj}: {time}" 
                                               for day, subj, time in schedule)
    else:
        day_schedule = [s for s in schedule if s[0] == text]
        text = f"🕒 Расписание на {text}:\n\n" + "\n".join(f"{subj}: {time}" 
                                                          for _, subj, time in day_schedule)
    
    bot.send_message(message.chat.id, text or "Расписание пусто", 
                    reply_markup=main_menu())
