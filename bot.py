import os
import asyncio
import requests

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart

TOKEN = "8576282694:AAE5jxF81AgEkL8LqkjyIvyXcv-ITv4XSl8"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Хранилище данных пользователей
user_data = {}


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "🎬 Привет! Я Tarantino 2.0\n\n"
        "Отправь фото."
    )


# Получение фото
@dp.message(F.photo)
async def handle_photo(message: Message):

    # Берем фото лучшего качества
    photo = message.photo[-1]

    # Получаем файл от Telegram
    file = await bot.get_file(photo.file_id)

    file_path = file.file_path

    # Ссылка на файл
    url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"

    # Скачиваем картинку
    img_data = requests.get(url).content

    # Создаем папку media если нет
    os.makedirs("media", exist_ok=True)

    # Имя файла
    filename = f"media/{message.from_user.id}.jpg"

    # Сохраняем файл
    with open(filename, "wb") as f:
        f.write(img_data)

    # Сохраняем данные пользователя
    user_data[message.from_user.id] = {
        "image": filename
    }

    await message.answer(
        "✅ Фото получено!\n\n"
        "Теперь отправь описание видео."
    )


# Получение текста
@dp.message()
async def handle_prompt(message: Message):

    # Проверяем есть ли фото
    if message.from_user.id not in user_data:
        await message.answer(
            "❌ Сначала отправь фото."
        )
        return

    prompt = message.text

    image_path = user_data[message.from_user.id]["image"]

    # Пока просто отправляем обратно фото
    await message.answer_photo(
        photo=open(image_path, "rb"),
        caption=f"🎬 Твой запрос:\n\n{prompt}"
    )


async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())