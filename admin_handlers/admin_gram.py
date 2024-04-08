from aiogram import Bot
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
import sqlite3
import re
from utils.state import Rass, City, Admin, Area, Item, Gram, Balance, Balance_del, Clad
import logging
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

async def admin_gram_menu(call: CallbackQuery, bot: Bot):
    try:
        key_item = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Добавить Фасовку", callback_data='add_gram_set_')
            ],
            [
                InlineKeyboardButton(text="Удалить Фасовку", callback_data='del_gram_set_')
            ],
            [
                InlineKeyboardButton(text="Просмотр Фасовки", callback_data='show_gram_set_')
            ],
            [
                InlineKeyboardButton(text="Назад", callback_data='admin_command')
            ]
        ])

        await bot.send_message(call.message.chat.id, "Выберите действие.", reply_markup=key_item)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

async def add_gram(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id
        await bot.send_message(user_id, f"Введите Граммовку:")
        await bot.delete_message(user_id, call.message.message_id)
        await state.set_state(Gram.name_gram)
    except:
        pass



async def add_gram_end(message: Message, bot: Bot, state: FSMContext):
    try:
        gram = message.text
        user_id = message.chat.id
        await bot.delete_message(user_id, message.message_id - 1)

        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO grams (gram) VALUES (?)", (gram,))

        # Применение изменений и закрытие соединения с базой данных
        conn.commit()
        conn.close()
        key_item = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
            ]
        ])
        await bot.send_message(user_id, f"Граммовка {gram} успешно добавлена! ✅", reply_markup=key_item)
        await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def del_gram(call: CallbackQuery, bot: Bot):
    try:
        user_id = call.message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT gram FROM grams")
        items = cursor.fetchall()
        conn.close()

        if len(items) == 0:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')], ])

            await bot.send_message(user_id, "Нет доступных Граммовок для удаления.", reply_markup=key_item)
            await bot.delete_message(user_id, call.message.message_id)

        else:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text=item[0], callback_data=f'_gram_del_{item[0]}') for item in items
                ],
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])

            await bot.send_message(user_id, f"Выберите Граммовку для удаления:", reply_markup=key_item)
            await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def del_gram_end(call: CallbackQuery, bot: Bot):
    try:
        user_id = call.message.chat.id
        gram = call.data.split('_')[3]
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM grams WHERE gram=?", (gram,))
        conn.commit()
        conn.close()
        key_item = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')], ])
        await bot.send_message(user_id, f"Граммовка: {gram} успешно удалёна! ✅", reply_markup=key_item)
        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def show_gram(call: CallbackQuery, bot: Bot):
    try:
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()

        # Выполняем SQL-запрос для получения всех админов
        cursor.execute('SELECT  id, gram FROM grams')
        grams = cursor.fetchall()

        # Закрываем соединение с базой данных
        conn.close()
        key_item = InlineKeyboardMarkup(inline_keyboard=[

            [InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')], ])
        if grams:
            message_text = "Список Граммовок:\n"
            for gram in grams:
                id_gram, name_gram = gram
                message_text += f"ID: {id_gram}\n"
                message_text += f"Граммовка: {name_gram}\n\n"

            await bot.send_message(call.message.chat.id, message_text, reply_markup=key_item)
            await bot.delete_message(call.message.chat.id, call.message.message_id)

        else:
            await bot.send_message(call.message.chat.id, "Нет Граммовок к просмотру.", reply_markup=key_item)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass