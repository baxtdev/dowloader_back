from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail 
from django.conf import settings
from asgiref.sync import async_to_sync


from telegram import Bot

from .models import News,Announcement,TelegramClient


@receiver(post_save, sender=News)
def send_news_notification(sender, instance, created, **kwargs):
    if created:
        bot = Bot(token=settings.TELEGRAM_TOKEN)
        news_title = instance.title
        news_content = instance.content
        news_image = instance.image.url if instance.image else None

        news_text = f'Новость: {news_title}\n\n{news_content}'

        if news_image:
            news_text += f'\nСсылка на изображение: {news_image}'

        for client in TelegramClient.objects.only('chat_id'):
            async_to_sync(bot.send_message)(chat_id=client.chat_id, text=news_text)

        print("все")    


@receiver(post_save, sender=Announcement)
def send_announcement_notification(sender, instance, created, **kwargs):
    if created:
        bot = Bot(token=settings.TELEGRAM_TOKEN)
        announcement_title = instance.title
        announcement_content = instance.content
        announcement_image = instance.image.url if instance.image else None

        announcement_text = f'Анонс: {announcement_title}\n\n{announcement_content}'

        if announcement_image:
            announcement_text += f'\nСсылка на изображение: {announcement_image}'

        for client in TelegramClient.objects.only('chat_id'):
            async_to_sync(bot.send_message)(chat_id=client.chat_id, text=announcement_text)

        print("все")