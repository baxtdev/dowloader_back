import instaloader
from pytube import YouTube
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    ConversationHandler,
    filters,
)
import yt_dlp


async def download_video_from_youtube(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict =  ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info_dict)


async def download_youtube_video(update: Update, context: CallbackContext):
            video_url = update.message.text.strip()

            try:
                yt = YouTube(video_url)
                video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()

                if not video_stream:
                    await update.message.reply_text("Не удалось найти подходящий поток для видео.")
                    return

                await update.message.reply_text("Скачиваю видео, подождите...")
                video_path = video_stream.url
                await update.message.reply_video(video=video_path)
            except Exception as e:
                await update.message.reply_text("Не удалось скачать видео. Проверьте ссылку и попробуйте снова.")




async def download_instagram_video(update: Update, context: CallbackContext):
            video_url = update.message.text.strip()
            loader = instaloader.Instaloader()

            try:
                post = instaloader.Post.from_shortcode(loader.context, video_url.split("/")[-2])
                video_link = post.video_url

                if not video_link:
                    await update.message.reply_text("Не удалось найти видео для скачивания.")
                    return

                await update.message.reply_text("Скачиваю видео, подождите...")
                await update.message.reply_video(video=video_link)
                return 0

            except Exception as e:
                await update.message.reply_text("Не удалось скачать видео. Проверьте ссылку и попробуйте снова.")
