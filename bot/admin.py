from django.contrib import admin

# Register your models here.
from .models import TelegramClient,News

@admin.register(TelegramClient)
class TelegramClientAdmin(admin.ModelAdmin):
    pass

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    pass