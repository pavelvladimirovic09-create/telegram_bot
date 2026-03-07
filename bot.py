from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

# Переменная окружения с токеном
TOKEN = os.getenv("TOKEN")

# Файл для хранения списка
FILE_NAME = "shopping_list.txt"

# Пользователи и история
users = set()
history = []

# Загрузка и сохранение списка
def load_list():
    try:
        with open(FILE_NAME, "r") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []

def save_list(shopping_list):
    with open(FILE_NAME, "w") as f:
        for item in shopping_list:
            f.write(item + "\n")

shopping_list = load_list()

# пользователи бота
users_set = set()

# история действий
history_list = []

# Клавиатура
keyboard = [
    ["➕ Добавить", "📋 Список"],
    ["❌ Удалить", "🗑 Очистить"],
    ["ℹ️ Помощь"]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.effective_user.username)
    await update.message.reply_text("Привет! Я бот для списка покупок.", reply_markup=reply_markup)

async def show_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if users:
        await update.message.reply_text("Участники бота:\n" + "\n".join(users))
    else:
        await update.message.reply_text("Пока никто не использует бота.")

async def last_changes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if history:
        await update.message.reply_text("Последние изменения:\n" + "\n".join(history[-5:]))
    else:
        await update.message.reply_text("Пока изменений нет.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.effective_user.username)
    text = update.message.text
    if text.startswith("➕ Добавить"):
        await update.message.reply_text("Отправь название продукта после команды /add")
    elif text.startswith("/add"):
        item = text.replace("/add ", "").strip()
        if item:
            shopping_list.append(item)
            save_list(shopping_list)
            history.append(f"{update.effective_user.username} добавил: {item}")
            await update.message.reply_text(f"{item} добавлен!")
    elif text.startswith("❌ Удалить"):
        await update.message.reply_text("Отправь название продукта после команды /remove")
    elif text.startswith("/remove"):
        item = text.replace("/remove ", "").strip()
        if item in shopping_list:
            shopping_list.remove(item)
            save_list(shopping_list)
            history.append(f"{update.effective_user.username} удалил: {item}")
            await update.message.reply_text(f"{item} удалён!")
        else:
            await update.message.reply_text("Такого элемента нет.")
    elif text.startswith("📋 Список"):
        if shopping_list:
            await update.message.reply_text("Список покупок:\n" + "\n".join(shopping_list))
        else:
            await update.message.reply_text("Список пуст.")
    elif text.startswith("🗑 Очистить"):
        shopping_list.clear()
        save_list(shopping_list)
        history.append(f"{update.effective_user.username} очистил список")
        await update.message.reply_text("Список очищен.")
    elif text.startswith("ℹ️ Помощь"):
        await update.message.reply_text(
            "Команды:\n"
            "/add <название> - добавить продукт\n"
            "/remove <название> - удалить продукт\n"
            "/users - показать участников\n"
            "/last - показать последние изменения"
        )

async def users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if users_set:
        users_list = "\n".join(users_set)
        await update.message.reply_text("Участники бота:\n" + users_list)
    else:
        await update.message.reply_text("Пока никто не пользовался ботом.")

# Создаём приложение
app = ApplicationBuilder().token(TOKEN).build()

# Добавляем обработчики
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("users", users_command))
app.add_handler(CommandHandler("users", show_users))
app.add_handler(CommandHandler("last", last_changes))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

# Запуск бота
print("Бот запущен...")
app.run_polling()
