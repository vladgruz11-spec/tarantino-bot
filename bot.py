import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("8576282694:AAE5jxF81AgEkL8LqkjyIvyXcv-ITv4XSl8")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Привет! Я Tarantino 2.0\n\n"
        "Отправь мне фото, а потом описание видео."
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Фото получил!\n\n"
        "Теперь отправь описание видео."
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🎥 Отлично, описание получил:\n\n{update.message.text}\n\n"
        "Следующим шагом подключим генерацию видео."
    )


def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN не найден в Railway Variables")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Бот запущен")
    app.run_polling()


if __name__ == "__main__":
    main()
