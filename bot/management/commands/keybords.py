from telegram import InlineKeyboardMarkup,InlineKeyboardButton,ReplyKeyboardMarkup



def get_main_menu_keyboard():
    buttons = [
        ['Tiktok', 'Instagram', 'YouTube'],
        ['Настройки']
    ]
    return ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
