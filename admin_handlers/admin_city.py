from aiogram import Bot
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
import sqlite3
import re
from utils.state import Rass, City, Admin, Area, Item, Gram, Balance, Balance_del, Clad
import logging
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta


async def admin_city_menu(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        key_city = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Добавить город", callback_data='add_city')
            ],
            [
                InlineKeyboardButton(text="Удалить город", callback_data='del_city')
            ],
            [
                InlineKeyboardButton(text="Просмотр городов", callback_data='show_city')
            ],
            [
                InlineKeyboardButton(text="Назад", callback_data='admin_command')
            ]
        ])

        await bot.send_message(call.message.chat.id, "Выберите действие.", reply_markup=key_city)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass


async def add_city(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Введите название Города:")
        await state.set_state(City.city_add)

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def add_city_end(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(city_add=message.text)

        context_data = await state.get_data()
        city_add = context_data.get('city_add')
        city = str(city_add)
        await bot.delete_message(user_id, message.message_id - 1)

        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO city (name_city) VALUES (?)", (city,))

        # Применение изменений и закрытие соединения с базой данных
        conn.commit()
        conn.close()
        key_city = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
            ]
        ])
        await bot.send_message(user_id, f"Город {city} успешно добавлен! ✅", reply_markup=key_city)
        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def del_city(call: CallbackQuery, bot: Bot):
    try:
        user_id = call.message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name_city FROM city")
        cities = cursor.fetchall()
        conn.close()

        if len(cities) == 0:
            key_city = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]

            ])

            await bot.send_message(user_id, "Нет доступных городов для удаления.", reply_markup=key_city)
            await bot.delete_message(user_id, call.message.message_id)

        else:
            key_city = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text=city[0], callback_data=f'_city_del_{city[0]}') for city in cities
                ],
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])

            await bot.send_message(user_id, f"Выберите город для удаления:", reply_markup=key_city)
            await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def del_city_end(call: CallbackQuery, bot: Bot):
    try:
        print(call)
        user_id = call.message.chat.id
        city = call.data.split('_')[3]
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM city WHERE name_city=?", (city,))
        conn.commit()
        conn.close()
        key_city = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
            ]
        ])
        await bot.send_message(user_id, f"Город {city} успешно удалён! ✅", reply_markup=key_city)
        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def show_city(call: CallbackQuery, bot: Bot):
    try:
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()

        # Выполняем SQL-запрос для получения всех админов
        cursor.execute('SELECT  id, name_city FROM city')
        citys = cursor.fetchall()

        # Закрываем соединение с базой данных
        conn.close()
        key_city = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
            ]
        ])
        if citys:
            message_text = "Список Городов:\n"
            for city in citys:
                id_city, name_city = city
                message_text += f"ID: {id_city}\n"
                message_text += f"Город: {name_city}\n\n"

            await bot.send_message(call.message.chat.id, message_text, reply_markup=key_city)
            await bot.delete_message(call.message.chat.id, call.message.message_id)

        else:
            await bot.send_message(call.message.chat.id, "Нет Городов к просмотру.", reply_markup=key_city)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
