from django.db import models

# Create your models here.

class TelegramClient(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=200, blank=True)
    user_id = models.IntegerField(unique=True)

    def __str__(self):
        return f'Chat ID: {self.chat_id}, Username: {self.username}'
    
    class Meta:
        verbose_name = 'Telegram Client'
        verbose_name_plural = 'Telegram Clients'


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to="blog/news/",blank=True,null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'


