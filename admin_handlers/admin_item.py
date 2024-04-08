
from aiogram import Bot
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
import sqlite3
import re
from utils.state import Rass, City, Admin, Area, Item, Gram, Balance, Balance_del, Clad
import logging
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta





async def admin_item_menu(call: CallbackQuery, bot: Bot):
    try:
        key_area = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Добавить Товар", callback_data='add_item_set_')
            ],
            [
                InlineKeyboardButton(text="Удалить Товар", callback_data='del_item_set_')
            ],
            [
                InlineKeyboardButton(text="Просмотр Товаров", callback_data='show_item_set_')
            ],
            [
                InlineKeyboardButton(text="Назад", callback_data='admin_command')
            ],
        ])

        await bot.send_message(call.message.chat.id, "Выберите действие.", reply_markup=key_area)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass


async def add_item(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id
        await state.set_state(Item.name_item)
        await bot.send_message(user_id, "Введите название Товара:")

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def add_item_center(message: Message, bot: Bot, state: FSMContext):
    try:
        item = message.text
        await state.set_state(Item.name_opis)
        await state.update_data(name_item=item)

        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, f"Введите Описание для товара {item}:")

        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_item_price(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id

        description = message.text
        await state.set_state(Item.price_item)
        await state.update_data(name_opis=description)
        context_data = await state.get_data()

        name_i = context_data.get('name_item')
        name_item = str(name_i)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, f"Отправьте цену товара ({name_item}) за грамм:")

        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_item_photo(message: Message, bot: Bot, state: FSMContext):
    try:
        price = message.text
        user_id = message.chat.id
        context_data = await state.get_data()
        await state.update_data(price_item=price)
        name_i = context_data.get('name_item')
        name_item = str(name_i)
        await bot.delete_message(user_id, message.message_id - 1)
        await bot.send_message(user_id, f"Отправьте фото для товара ({name_item}):")
        await state.set_state(Item.photo_item)
        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_item_end(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        photo = message.photo[-1].file_id
        await state.update_data(photo_item=photo)
        context_data = await state.get_data()
        name_i = context_data.get('name_item')
        name_item = str(name_i)
        name_o = context_data.get('name_opis')
        name_opis = str(name_o)
        price_i = context_data.get('price_item')
        price_item = str(price_i)
        await bot.delete_message(message.chat.id, message.message_id - 1)
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO item (name_item, caption_item, price_item, photo_item) VALUES (?, ?, ?, ?)",
                       (name_item, name_opis, price_item, photo))

        conn.commit()
        conn.close()
        key_item = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
            ]
        ])
        await bot.send_message(user_id, f" Товар {name_item} успешно добавлен! ✅\n"
                                        f"Описание : {name_opis}\n"
                                        f"Цена: {price_item}\n", reply_markup=key_item)
        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def del_item(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name_item FROM item")
        items = cursor.fetchall()
        conn.close()

        if len(items) == 0:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])

            await bot.send_message(user_id, "Нет доступных Товаров для удаления.", reply_markup=key_item)
            await bot.delete_message(user_id, call.message.message_id)

        else:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text=item[0], callback_data=f'_item_del_{item[0]}') for item in items
                ],
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])
            await bot.send_message(user_id, f"Выберите Товар для удаления:", reply_markup=key_item)
            await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def del_item_end(call: CallbackQuery, bot: Bot):
    try:
        user_id = call.message.chat.id
        item = call.data.split('_')[3]
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM item WHERE name_item=?", (item,))
        conn.commit()
        conn.close()
        key_item = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
            ]
        ])
        await bot.send_message(user_id, f"Товар: {item} успешно удалён! ✅", reply_markup=key_item)
        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def show_item(call: CallbackQuery, bot: Bot):
    try:
        user_id = call.message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name_item FROM item")
        items = cursor.fetchall()
        conn.close()

        if len(items) == 0:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])
            await bot.send_message(user_id, "Нет доступных Товаров для просмотров.", reply_markup=key_item)
            await bot.delete_message(user_id, call.message.message_id)

        else:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text=item[0], callback_data=f'_item_show_{item[0]}') for item in items
                ],
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])

            await bot.send_message(user_id, f"Выберите Товар для просмотра информации:", reply_markup=key_item)
            await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def show_end(call: CallbackQuery, bot: Bot):
    try:
        user_id = call.message.chat.id
        item = call.data.split('_')[3]

        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name_item, caption_item, photo_item FROM item WHERE name_item=?", (item,))
        item_info = cursor.fetchone()
        conn.close()
        key_item = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
            ]

        ])
        if item_info:
            photo_data = item_info[2]  # Данные фотографии в виде BLOB
            await bot.send_photo(call.message.chat.id, photo_data, caption=f"Товар: {item_info[0]}\n"
                                                                           f"Описание: {item_info[1]}",
                                 reply_markup=key_item)
            await bot.delete_message(user_id, call.message.message_id)
        else:
            await bot.send_message(user_id, f"Нет информации о товаре{item_info[0]}", reply_markup=key_item)
            await bot.delete_message(user_id, call.message.message_id)
    except:
        pass
