from aiogram import Bot
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
import sqlite3
import re
from utils.state import Rass, City, Admin, Area, Item, Gram, Balance, Balance_del, Clad
import logging
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

async def admin_area_menu(call: CallbackQuery, bot: Bot):
    try:
        key_area = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Добавить район", callback_data='add_area_set_'),
            ],
            [
                InlineKeyboardButton(text="Удалить район", callback_data='del_area_set_')

            ],
            [
                InlineKeyboardButton(text="Просмотр райнов", callback_data='show_area_set_'),

            ],
            [
                InlineKeyboardButton(text="Назад", callback_data='admin_command')
            ]
        ])

        await bot.send_message(call.message.chat.id, "Выберите действие.", reply_markup=key_area)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass


async def add_area(call: CallbackQuery, bot: Bot):
    try:
        user_id = call.message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name_city FROM city")
        cities = cursor.fetchall()
        conn.close()

        if len(cities) == 0:
            key_area = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command'),
                ]
            ])
            await bot.send_message(user_id, "Для продолжения добавьте сначала Город.", reply_markup=key_area)
            await bot.delete_message(user_id, call.message.message_id)

        else:
            key_area = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text=city[0], callback_data=f'_city_area_{city[0]}') for city in cities

                ],
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])

            await bot.send_message(user_id, f"Выберите город :", reply_markup=key_area)
            await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def add_area_central(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id
        city = call.data.split('_')[3]
        await state.set_state(Area.name_area)
        await state.update_data(name_city=city)

        await bot.send_message(user_id, f"Введите название Района для города {city}:")

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def add_area_end(message: Message, state: FSMContext, bot: Bot):
    try:
        area = message.text
        user_id = message.chat.id
        await state.update_data(name_area=message.text)
        context_data = await state.get_data()
        area_name = context_data.get('name_area')
        city_name = context_data.get('name_city')
        area_n = str(area_name)
        city_n = str(city_name)
        await bot.delete_message(user_id, message.message_id - 1)
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO area (name_city, name_area) VALUES (?, ?)", (city_n, area_n))
        conn.commit()
        conn.close()
        key_area = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
            ]
        ])
        await bot.send_message(user_id, f"В Город {city_n} успешно добавлен район {area}! ✅", reply_markup=key_area)
        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def del_area(call: CallbackQuery, bot: Bot):
    try:
        user_id = call.message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name_area FROM area")
        areas = cursor.fetchall()
        conn.close()

        if len(areas) == 0:
            key_area = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])

            await bot.send_message(user_id, "Нет доступных Районов для удаления.", reply_markup=key_area)
            await bot.delete_message(user_id, call.message.message_id)

        else:
            key_area = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text=area[0], callback_data=f'/area/del/{area[0]}') for area in areas
                ],
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])
            await bot.send_message(user_id, f"Выберите Район для удаления:", reply_markup=key_area)
            await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def del_area_end(call: CallbackQuery, bot: Bot):
    try:
        user_id = call.message.chat.id
        area = call.data.split('/')[3]
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        print(area)
        cursor.execute("DELETE FROM area WHERE name_area=?", (area,))
        conn.commit()
        conn.close()
        key_area = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
            ]
        ])
        await bot.send_message(user_id, f"Район: {area} успешно удалён! ✅", reply_markup=key_area)
        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def show_area(call: CallbackQuery, bot: Bot):
    try:
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute('SELECT  id, name_city, name_area FROM area')
        areas = cursor.fetchall()
        conn.close()
        key_area = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
            ]
        ])
        if areas:
            message_text = "Список Райнов:\n"
            for area in areas:
                id_area, name_city, name_area = area
                message_text += f"ID: {id_area}\n"
                message_text += f"Город: {name_city}\n"
                message_text += f"Район: {name_area}\n\n"

            await bot.send_message(call.message.chat.id, message_text, reply_markup=key_area)
            await bot.delete_message(call.message.chat.id, call.message.message_id)

        else:
            await bot.send_message(call.message.chat.id, "Нет Райнов к просмотру.", reply_markup=key_area)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass