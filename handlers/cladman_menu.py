from aiogram import Bot
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
import sqlite3
import re
from utils.state import CladManJob
import logging
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

async def cladman_menu(message: Message, bot: Bot):
    try:
        key_item = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Добавить Клад", callback_data='cm_cl')
            ],
            [
                InlineKeyboardButton(text="Назад", callback_data='admin_command')
            ],
        ])

        await bot.send_message(message.chat.id, "Выберите действие.", reply_markup=key_item)
        await bot.delete_message(message.chat.id, message.message_id)
    except:
        pass


async def add_clad_cladman(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name_city FROM city")
        items = cursor.fetchall()
        conn.close()

        if len(items) == 0:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')]
            ])
            await bot.send_message(user_id, "Нет доступных Городов", reply_markup=key_item)
            await bot.delete_message(user_id, call.message.message_id)



        else:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text=item[0], callback_data=f'_cladman_city_{item[0]}') for item in items
                ],
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])

            await bot.send_message(user_id, f"Выберите Город для добавление клада:", reply_markup=key_item)
            await bot.delete_message(user_id, call.message.message_id)
    except:
        pass

async def add_clad_area_cladman(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        city = call.data.split('_')[3]
        await state.update_data(city_clad=city)

        user_id = call.message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name_area FROM area")
        items = cursor.fetchall()
        conn.close()

        if len(items) == 0:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])
            await bot.send_message(user_id, "Нет доступных Районов", reply_markup=key_item)
            await bot.delete_message(user_id, call.message.message_id)

        else:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text=item[0], callback_data=f'_cladman_area_{city}_{item[0]}') for item in items
                ],
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])
            await bot.send_message(user_id, f"Выберите Район для добавление клада:", reply_markup=key_item)
            await bot.delete_message(user_id, call.message.message_id)
    except:
        pass

async def add_clad_item_cladman(call: CallbackQuery, bot: Bot):
    try:
        city = call.data.split('_')[3]
        area = call.data.split('_')[4]

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

            await bot.send_message(user_id, "Нет доступных Товаров", reply_markup=key_item)
            await bot.delete_message(user_id, call.message.message_id)

        else:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text=item[0],
                                         callback_data=f'_cladman_item_{city}_{area}_{item[0]}') for item in items
                ],
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])

            await bot.send_message(user_id, f"Выберите Товар для добавление клада:", reply_markup=key_item)
            await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def add_clad_gram_cladman(call: CallbackQuery, bot: Bot):
    try:
        city = call.data.split('_')[3]
        area = call.data.split('_')[4]
        tovar = call.data.split('_')[5]

        user_id = call.message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT gram FROM grams")
        items = cursor.fetchall()
        conn.close()

        if len(items) == 0:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [

                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])

            await bot.send_message(user_id, "Нет доступных Граммовок", reply_markup=key_item)
            await bot.delete_message(user_id, call.message.message_id)

        else:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text=item[0],
                                         callback_data=f'_cladman_gram_{city}_{area}_{tovar}_{item[0]}') for item in items
                ],
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])

            await bot.send_message(user_id, f"Выберите Граммовку для добавление клада:", reply_markup=key_item)
            await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def add_clad_grams_cladman(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        city = call.data.split('_')[3]
        area = call.data.split('_')[4]
        tovar = call.data.split('_')[5]
        gram = call.data.split('_')[6]
        await state.update_data(area_clad=area)
        await state.update_data(tovar_clad=tovar)
        await state.update_data(gram_clad=gram)

        await state.set_state(CladManJob.latit)
        user_id = call.message.chat.id
        await bot.send_message(user_id, f"Введите Цену для товара ({tovar}) Граммовка ({gram}):")
        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def add_clad_lat_cladman(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        price = message.text

        await state.update_data(price_clad=price)
        await state.set_state(CladManJob.longtit)

        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, f"Введите Широту Координат (**,******)")
        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_clad_long_cladman(message: Message, bot: Bot, state: FSMContext):
    try:
        latitude = message.text
        await state.update_data(latit=latitude)
        await state.set_state(CladManJob.longdob)

        user_id = message.chat.id
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, f"Введите Долготу Координат (**,******)")
        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_clad_photo_cladman(message: Message, bot: Bot, state: FSMContext):
    try:
        longtitude = message.text
        await state.update_data(longtit=longtitude)
        await state.set_state(CladManJob.photo_clad)

        user_id = message.chat.id
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, f"Отправьте фото клада:")
        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_clad_end_cladman(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        context_data = await state.get_data()
        city_add = context_data.get('city_clad')
        city = str(city_add)
        area_add = context_data.get('area_clad')
        area = str(area_add)
        tovar_add = context_data.get('tovar_clad')
        tovar = str(tovar_add)
        gram_add = context_data.get('gram_clad')
        gram = str(gram_add)
        price_add = context_data.get('price_clad')
        price = str(price_add)
        latitude_add = context_data.get('latit')
        latitude = str(latitude_add)
        longtitude_add = context_data.get('longtit')
        longtitude = str(longtitude_add)
        if message.photo:
            photo_url = message.photo[-1].file_id
        else:
            photo_url = None
        await bot.delete_message(message.chat.id, message.message_id - 1)
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clad (name_city, name_area, name_item, name_gram, price_item, latitude, longtitude, photo_clad) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (city, area, tovar, gram, price, latitude, longtitude, photo_url))

        # Применение изменений и закрытие соединения с базой данных
        conn.commit()
        conn.close()
        key_item = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='back_menu_st_')
            ]
        ])
        await bot.send_photo(message.chat.id, photo_url, caption=f" Город: {city}\n"
                                                                 f"Район:{area}\n"
                                                                 f"Товар:{tovar}\n"
                                                                 f"Граммовка:{gram}\n"
                                                                 f"Цена:{price}\n"
                                                                 f"Долгота:{latitude}\n"
                                                                 f"Широта:{longtitude}\n"
                                                                 f"Клад успешно добавлен! ✅", reply_markup=key_item)
        await bot.delete_message(user_id, message.message_id)
    except:
        pass