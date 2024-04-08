from aiogram import Bot
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
import sqlite3
import re
from utils.state import CladMan
import logging
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

async def admin_cladman_menu(call: CallbackQuery, bot: Bot):
    try:
        key_area = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Добавить кладмэна", callback_data='add_cladman'),
            ],
            [
                InlineKeyboardButton(text="Удалить кладмэна", callback_data='del_cladman')

            ],
            [
                InlineKeyboardButton(text="Просмотр кладмэнов", callback_data='show_cladman'),

            ],
            [
                InlineKeyboardButton(text="Назад", callback_data='admin_command')
            ]
        ])

        await bot.send_message(call.message.chat.id, "Выберите действие.", reply_markup=key_area)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass


async def admin_cladman(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id
        await bot.send_message(user_id, "Введите Имя для добавление кладмэна:")
        await state.set_state(CladMan.name_cladman)

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def admin_cladman_mid(message: Message, state: FSMContext, bot: Bot):
    try:
        await state.update_data(name_cladman=message.text)
        user_id = message.chat.id
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Введите external_id для добавление в админы:")
        await state.set_state(CladMan.external_id_cladman)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def admin_cladman_end(message: Message, state: FSMContext, bot: Bot):
    try:
        await state.update_data(admin_id=message.text)
        user_id = message.chat.id
        context_data = await state.get_data()

        admin_name = context_data.get('name_cladman')
        admin_id = context_data.get('admin_id')
        admin_nm = str(admin_name)
        admin_i = str(admin_id)
        await bot.delete_message(user_id, message.message_id - 1)

        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO cladman (name_cladman, external_cladman) VALUES (?, ?)', (admin_nm, admin_i))

        conn.commit()

        # Закрываем соединение с базой данных
        conn.close()
        key_admin = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
            ]

        ])
        await bot.send_message(user_id, f"Кладмэн {admin_nm} добавлен в базу.", reply_markup=key_admin)
        await bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

async def admin_show_cladman(call: CallbackQuery, bot: Bot):
    try:
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()

        # Выполняем SQL-запрос для получения всех админов
        cursor.execute('SELECT id, name_cladman, external_cladman FROM cladman')
        admins = cursor.fetchall()

        # Закрываем соединение с базой данных
        conn.close()
        key_city = InlineKeyboardMarkup(inline_keyboard=[

            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
            ]
        ])
        if admins:
            message_text = "Список кладмэнов:\n"
            for admin in admins:
                admin_id, name_admin, external_admin = admin
                message_text += f"ID: {admin_id}\n"
                message_text += f"Имя: {name_admin}\n"
                message_text += f"External ID: {external_admin}\n\n"

            await bot.send_message(call.message.chat.id, message_text, reply_markup=key_city)
            await bot.delete_message(call.message.chat.id, call.message.message_id)

        else:
            await bot.send_message(call.message.chat.id, "Нет зарегистрированных админов.", reply_markup=key_city)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass


async def del_cladman(call: CallbackQuery, bot: Bot):
    try:
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()

        cursor.execute("SELECT name_cladman FROM cladman")

        admin_names = cursor.fetchall()

        # Закрытие соединения с базой данных
        conn.close()

        key_admin = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=admin_name[0], callback_data=f'_cladman_del_{admin_name[0]}') for admin_name in
                admin_names
            ],
            [
                InlineKeyboardButton(text="Назад", callback_data='admin_command')
            ]

        ])

        await bot.send_message(call.message.chat.id, "Выберите кладмэна для удаления:", reply_markup=key_admin)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass


async def del_cladman_end(call: CallbackQuery, bot: Bot):
    try:
        admin_name = call.data.split('_')[3]
        print(admin_name)
        user_id = call.message.chat.id
        conn = sqlite3.connect('shop.db')  # баз данных
        cursor = conn.cursor()

        cursor.execute("DELETE FROM admin WHERE name_admin = ?", (admin_name,))

        # Сохраняем изменения
        conn.commit()

        # Закрываем соединение с базой данных
        conn.close()
        key_admin = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
            ]
        ])
        await bot.send_message(user_id, f"Вы успешно удалили кладмэна : {admin_name}", reply_markup=key_admin)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

