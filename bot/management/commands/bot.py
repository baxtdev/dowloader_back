from django.conf import settings
from django.core.management.base import BaseCommand

from asgiref.sync import sync_to_async
import logging
import os

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    ConversationHandler,
    filters,
)

from tiktok_downloader import TTDownloader
import instaloader
from pytube import YouTube

from ...models import TelegramClient
from .keybords import get_main_menu_keyboard
from .services import download_instagram_video, download_youtube_video,download_video_from_youtube

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

PLATFORM, URL = range(2)

class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **kwargs):
        application = Application.builder().token(settings.TELEGRAM_TOKEN).build()

        async def start(update: Update, context: CallbackContext):
            user_id = update.message.from_user.id
            chat_id = update.message.chat_id
            username = update.message.from_user.username
            client, _ = await sync_to_async(TelegramClient.objects.get_or_create)(
                chat_id=chat_id,
                username=username,
                user_id=user_id,
            )
            await update.message.reply_text(
                "Привет! Я могу скачать видео без водяного знака.\n"
                "Выберите платформу для скачивания:",
                reply_markup=ReplyKeyboardMarkup(
                    [['Instagram', 'TikTok', 'YouTube']],
                    one_time_keyboard=True, resize_keyboard=True
                )
            )
            return PLATFORM

        async def platform_choice(update: Update, context: CallbackContext):
            platform = update.message.text
            context.user_data['platform'] = platform
            await update.message.reply_text(
                f"Вы выбрали {platform}. Пожалуйста, отправьте ссылку на видео.",
                reply_markup=ReplyKeyboardRemove()
            )
            return URL

        async def download_video(update: Update, context: CallbackContext):
            platform = context.user_data['platform']
            video_url = update.message.text
            logger.info(f"Платформа: {platform}, URL: {video_url}")

            try:
                if platform == 'TikTok':
                    video = TTDownloader(video_url)
                    media_info = video.get_media()

                    if not media_info:
                        await update.message.reply_text("Не удалось найти медиафайлы для скачивания.")
                        return await prompt_platform_choice(update)

                    _video = media_info[0].__dict__
                    video_url = _video['json']
                    await update.message.reply_text("Скачиваю видео, подождите...")
                    await update.message.reply_video(video=video_url)

                elif platform == 'YouTube':
                    video_path = download_video_from_youtube(video_url)
                    with open(video_path, 'rb') as video_file:
                        update.message.reply_video(video_file)

                    os.remove(video_path)

                elif platform == 'Instagram':
                    video_url = update.message.text.strip()
                    loader = instaloader.Instaloader()
                    post = instaloader.Post.from_shortcode(loader.context, video_url.split("/")[-2])
                    video_link = post.video_url
                    if not video_link:
                        await update.message.reply_text("Не удалось найти видео для скачивания.")
                        return await prompt_platform_choice(update)
                    await update.message.reply_text("Скачиваю видео, подождите...")
                    await update.message.reply_video(video=video_link)

            except Exception as e:
                logger.error(f"Ошибка при скачивании видео: {e}")
                await update.message.reply_text("Не удалось скачать видео. Проверьте ссылку и попробуйте снова.")
                return await prompt_platform_choice(update)

            return await prompt_platform_choice(update)

        async def prompt_platform_choice(update: Update):
            """Функция для запроса платформы после скачивания или ошибки"""
            await update.message.reply_text(
                "Выберите платформу для скачивания:",
                reply_markup=ReplyKeyboardMarkup(
                    [['Instagram', 'TikTok', 'YouTube']],
                    one_time_keyboard=True, resize_keyboard=True
                )
            )
            return PLATFORM

        async def error_handler(update: object, context: CallbackContext):
            logger.error(f"Произошла ошибка: {context.error}")

        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                PLATFORM: [MessageHandler(filters.TEXT & ~filters.COMMAND, platform_choice)],
                URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, download_video)],
            },
            fallbacks=[],
        )

        application.add_handler(conversation_handler)
        application.add_error_handler(error_handler)

        logger.info("Бот запущен...")
        application.run_polling()
