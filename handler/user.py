import telebot
import random

from funcs.db import get_books_from_db, save_data, delete_data
from init_bot import bot


class UserState(telebot.handler_backends.StatesGroup):
    note = telebot.handler_backends.State()
    note_id = telebot.handler_backends.State()


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = (f"Привет, этот бот создан для заметок\n"
            f"/get_notes - Мои заметки\n"
            f"/add_note - Добавить заметку\n"
            f"/delete_note - Удалить заметку")
    bot.send_message(message.chat.id, text=text)


@bot.message_handler(commands=['get_notes'])
def get_book(message: telebot.types.Message):
    user_id = int(message.from_user.id)
    books = get_books_from_db(user_id)
    if books == []:
        bot.send_message(message.from_user.id, "Заметок нет")
    else:
        for i in range(len(books)):
            bot.send_message(message.chat.id, f"Заметка {books[i][1]}\n"
                                            f"{books[i][2]}")
            print(books[i])


@bot.message_handler(commands=['add_note'])
def pr(message: telebot.types.Message):
    bot.set_state(message.from_user.id, UserState.note, message.chat.id)


@bot.message_handler(state=UserState.note)
def st(message: telebot.types.Message):
    with bot.retrieve_data(message.from_user.id) as data:
        data['note'] = message.text
    data_text = data['note']
    user_id = int(message.from_user.id)
    save_data(id=user_id, s=data_text)
    bot.send_message(message.from_user.id, "Заметка сохранена")
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(commands=['delete_note'])
def delete(message: telebot.types.Message):
    bot.send_message(message.from_user.id, "Напишите номер заметки, которую хотите удалить")
    bot.set_state(message.from_user.id, UserState.note_id, message.chat.id)


@bot.message_handler(state=UserState.note_id)
def state1(message: telebot.types.Message):
    with bot.retrieve_data(message.from_user.id) as data:
        data['note_id'] = message.text
    try:
        note_id = int(data['note_id'])
    except Exception:
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.from_user.id, "Вы ввели не число!")
        bot.set_state(message.from_user.id, UserState.note_id, message.chat.id)
    else:
        user_id = int(message.from_user.id)
        if get_books_from_db(user_id) == []:
            bot.send_message(message.from_user.id, "Удалять нечего")
        else:
            delete_data(note_id, user_id)
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.from_user.id, f"Заметка {note_id} удалена")


@bot.message_handler(state='*')
def stat(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Список команд:\n"
                                      "/get_notes - Мои заметки\n"
                                      "/add_note - Добавить заметку\n"
                                      "/delete_note - Удалить заметку")