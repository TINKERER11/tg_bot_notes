from funcs.db import create_databases
from handler import register_handlers
from init_bot import bot
import telebot

if __name__ == "__main__":
    create_databases()
    register_handlers()
    print("Бот запущен")
    bot.add_custom_filter(telebot.custom_filters.StateFilter(bot))
    bot.infinity_polling()
