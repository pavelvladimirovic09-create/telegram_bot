from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from datetime import datetime

TOKEN = "8642952909:AAFH8Hc9t_TqKtiT_ib8wUzCJiiF4Ai6C-s"

shopping_list = []

keyboard = [
    ["➕ Добавить", "📋 Список"],
    ["❌ Удалить", "✅ Куплено"],
    ["🗑 Очистить"]
]

markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Бот списка покупок",
        reply_markup=markup
    )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text


# ДОБАВИТЬ
    if text == "➕ Добавить":

        context.user_data["adding"] = True
        context.user_data["deleting"] = False
        context.user_data["buying"] = False

        await update.message.reply_text("Напишите товары через запятую")


# ВВОД ТОВАРОВ
    elif context.user_data.get("adding"):

        items = [i.strip() for i in text.split(",")]

        username = update.effective_user.first_name
        date_now = datetime.now().strftime("%d.%m.%Y %H:%M")

        added = []

        for item in items:
            if item:

                item_full = f"{item} — {date_now} ({username})"

                shopping_list.append(item_full)
                added.append(item)

        context.user_data["adding"] = False

        await update.message.reply_text(
            "Добавлено: " + ", ".join(added),
            reply_markup=markup
        )


# СПИСОК
    elif text == "📋 Список":

        if shopping_list:

            message = ""

            for i, item in enumerate(shopping_list, start=1):
                message += f"{i}. {item}\n"

            await update.message.reply_text(message)

        else:
            await update.message.reply_text("Список пуст")


# УДАЛИТЬ
    elif text == "❌ Удалить":

        context.user_data["deleting"] = True
        context.user_data["adding"] = False
        context.user_data["buying"] = False

        await update.message.reply_text("Напишите номер позиции для удаления")


# ВВОД НОМЕРА ДЛЯ УДАЛЕНИЯ
    elif context.user_data.get("deleting"):

        if text.isdigit():

            number = int(text)

            if 1 <= number <= len(shopping_list):

                removed = shopping_list.pop(number - 1)

                await update.message.reply_text(
                    f"Удалено: {removed}",
                    reply_markup=markup
                )

            else:
                await update.message.reply_text("Нет такого номера")

        else:
            await update.message.reply_text("Введите номер")

        context.user_data["deleting"] = False


# КУПЛЕНО
    elif text == "✅ Куплено":

        context.user_data["buying"] = True
        context.user_data["adding"] = False
        context.user_data["deleting"] = False

        await update.message.reply_text("Напишите номер купленного товара")


# ОТМЕТИТЬ КУПЛЕННЫМ
    elif context.user_data.get("buying"):

        if text.isdigit():

            number = int(text)

            if 1 <= number <= len(shopping_list):

                item = shopping_list[number - 1]

                shopping_list[number - 1] = f"~~{item}~~ ✅"

                await update.message.reply_text(
                    "Отмечено как куплено",
                    reply_markup=markup
                )

            else:
                await update.message.reply_text("Нет такого номера")

        else:
            await update.message.reply_text("Введите номер")

        context.user_data["buying"] = False


# ОЧИСТИТЬ
    elif text == "🗑 Очистить":

        shopping_list.clear()

        await update.message.reply_text("Список очищен")


if __name__ == "__main__":

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("Бот запущен...")

    app.run_polling()
