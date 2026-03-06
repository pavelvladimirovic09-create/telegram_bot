from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from config import TOKEN

FILE_NAME = "shopping_list.txt"

def load_list():
    try:
        with open(FILE_NAME, "r") as f:
            return [line.strip() for line in f.readlines()]
    except:
        return []

def save_list():
    with open(FILE_NAME, "w") as f:
        for item in shopping_list:
            f.write(item + "\n")

shopping_list = load_list()
waiting_for_item = False

keyboard = [
    ["➕ Добавить", "📋 Список"],
    ["❌ Удалить", "🗑 Очистить"],
    ["ℹ️ Помощь"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я семейный бот покупок 🏠",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Используй кнопки для управления списком покупок",
        reply_markup=reply_markup
    )

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global waiting_for_item

    text = update.message.text
    user = update.effective_user.first_name

    if text == "➕ Добавить":
        waiting_for_item = True
        await update.message.reply_text("Напиши товар")

    elif text == "📋 Список":
        if shopping_list:
            text_list = "\n".join(f"{i+1}. {item}" for i, item in enumerate(shopping_list))
            await update.message.reply_text("Список покупок:\n" + text_list)
        else:
            await update.message.reply_text("Список пуст")

    elif text == "❌ Удалить":
        if shopping_list:
            text_list = "\n".join(f"{i+1}. {item}" for i, item in enumerate(shopping_list))
            await update.message.reply_text("Напиши номер товара для удаления:\n" + text_list)
            context.user_data["delete_mode"] = True
        else:
            await update.message.reply_text("Список пуст")

    elif text == "🗑 Очистить":
        shopping_list.clear()
        save_list()
        await update.message.reply_text("Список очищен")

    elif text == "ℹ️ Помощь":
        await update.message.reply_text(
            "Этот бот помогает семье вести список покупок 🛒",
            reply_markup=reply_markup
        )

    elif waiting_for_item:
        shopping_list.append(f"{text} — {user}")
        save_list()
        waiting_for_item = False
        await update.message.reply_text("Товар добавлен")

    elif context.user_data.get("delete_mode"):
        try:
            index = int(text) - 1
            removed = shopping_list.pop(index)
            save_list()
            await update.message.reply_text(f"Удалено: {removed}")
        except:
            await update.message.reply_text("Неверный номер")

        context.user_data["delete_mode"] = False

    else:
        await update.message.reply_text("Используй кнопки ниже", reply_markup=reply_markup)


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

    print("Бот запущен...")
    app.run_polling()
