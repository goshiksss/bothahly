import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram import Router
from datetime import datetime
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Данные бота (заданы вручную)
TOKEN = "7801959319:AAG3UtSdQWTrnPqk9NMNYR0rwcF1SipEAGk"
TARGET_CHAT_ID = -1002544018915  # ID целевого чата/канала
IGNORED_USER_ID = 1825028508      # ID пользователя, которого нужно игнорировать

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

# Функция для получения тега для медиа-сообщений
def get_media_tag(message: Message) -> str:
    if message.photo:
        return "#Фото"
    elif message.video_note:
        return "#кружочки"
    elif message.video:
        return "#Видео"
    elif message.voice:
        return "#Голосовое"
    return ""

# Создание маршрутизатора
router = Router()

# Обработчик для медиа-сообщений
@router.message(F.photo | F.video | F.video_note | F.voice)
async def forward_media(message: Message):
    if message.from_user.id == IGNORED_USER_ID:
        return  # Игнорируем сообщения указанного пользователя

    tag = get_media_tag(message)

    if message.photo:
        # Пересылаем фото с подписью
        caption = (message.caption or "") + f"\n\n{tag}"
        await bot.send_photo(TARGET_CHAT_ID, message.photo[-1].file_id, caption=caption)

    elif message.video:
        # Пересылаем видео с подписью
        caption = (message.caption or "") + f"\n\n{tag}"
        await bot.send_video(TARGET_CHAT_ID, message.video.file_id, caption=caption)

    else:
        # Для голосовых сообщений и видеокружков пересылаем отдельно и добавляем тег в ответе
        forwarded_message = await message.forward(TARGET_CHAT_ID)
        await bot.send_message(TARGET_CHAT_ID, tag, reply_to_message_id=forwarded_message.message_id)

# Регистрация маршрутов
dp.include_router(router)

# Функция для старта бота
async def start_bot():
    await dp.start_polling(bot)

async def run_continuous():
    while True:
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.info(f"Bot running at {current_time}")
            await dp.start_polling(bot)
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            await asyncio.sleep(60)  # Wait 1 minute before retrying

if __name__ == "__main__":
    try:
        asyncio.run(run_continuous())
    except KeyboardInterrupt:
        logging.info("Bot has been stopped.")