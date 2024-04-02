import telebot
import random

from funcs.db import get_books_from_db, save_data, delete_data, prov_1
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
    notes = get_books_from_db(user_id)
    if len(notes) == 0:
        bot.send_message(message.from_user.id, "Заметок нет")
    else:
        for i in range(len(notes)):
            bot.send_message(message.chat.id, f"Заметка {i + 1}\n"
                                              f"{notes[i][2]}")
            #print(notes[i])


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
    user_id = int(message.from_user.id)
    notes = get_books_from_db(user_id)
    if len(notes) == 0:
        bot.send_message(message.from_user.id, "Заметок нет")
    else:
        bot.send_message(message.from_user.id, "Напишите номер заметки, которую хотите удалить")
        bot.set_state(message.from_user.id, UserState.note_id, message.chat.id)


@bot.message_handler(state=UserState.note_id)
def state1(message: telebot.types.Message):
    user_id = int(message.from_user.id)
    notes = get_books_from_db(user_id)
    with bot.retrieve_data(message.from_user.id) as data:
        data['note_id'] = message.text
    try:
        note_id = int(data['note_id'])
    except ValueError:
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.from_user.id, "Вы ввели не число!")
        bot.set_state(message.from_user.id, UserState.note_id, message.chat.id)
    else:
        try:
            if len(prov_1(notes[note_id - 1][1], user_id)) == 0:
                bot.send_message(message.from_user.id, "Заметка не найдена")
                bot.delete_state(message.from_user.id, message.chat.id)
        except IndexError:
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.from_user.id, "Заметка не найдена")
            bot.set_state(message.from_user.id, UserState.note_id, message.chat.id)
        else:
            delete_data(notes[note_id - 1][1], user_id)
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.from_user.id, f"Заметка {note_id} удалена")


@bot.message_handler(state='*')
def stat(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Список команд:\n"
                                      "/get_notes - Мои заметки\n"
                                      "/add_note - Добавить заметку\n"
                                      "/delete_note - Удалить заметку")
