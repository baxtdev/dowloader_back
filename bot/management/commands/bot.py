from django.conf import settings
from django.core.management.base import BaseCommand

from asgiref.sync import sync_to_async
import logging

from telegram import Update, ReplyKeyboardMarkup,CallbackQuery
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    ConversationHandler,
    filters,
    CallbackQueryHandler,
)
from tiktok_downloader import TTDownloader


from ...models import TelegramClient




class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **kwargs):
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
            )
        logger = logging.getLogger(__name__)

        application = Application.builder().token(settings.TELEGRAM_TOKEN).build()

        async def start(update: Update, context):
            user_id = update.message.from_user.id
            chat_id = update.message.chat_id
            username = update.message.from_user.username
            client,_  = await sync_to_async(TelegramClient.objects.get_or_create)(
                chat_id=chat_id,
                username=username,
                user_id=user_id,
            )

            await update.message.reply_text(
        "Привет! Я могу скачать видео из TikTok без водяного знака.\n"
        "Отправь мне ссылку на видео, и я скачаю его для тебя."
        )

        async def download_tiktok_video(update: Update, context):
            message = update.message
            video_url = message.text

            try:
                video = TTDownloader(video_url)
                media_info = video.get_media()

                if not media_info:
                    await message.reply_text("Не удалось найти медиафайлы для скачивания.")
                    return

                _video = media_info[0].__dict__
                video_url = _video['json']
                await message.reply_text("Скачиваю видео, подождите...")
                await message.reply_video(video=video_url)

            except Exception as e:
                logger.error(f"Ошибка при скачивании видео: {e}")
                await message.reply_text("Не удалось скачать видео. Проверьте ссылку и попробуйте снова.")    

        async def error_handler(update: object, context):
            logger.error("Произошла ошибка: %s", context.error)


        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_tiktok_video))
        application.add_error_handler(error_handler)
        logger.info("Бот запущен...")

        application.run_polling()