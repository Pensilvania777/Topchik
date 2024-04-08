from aiogram import Bot
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
import sqlite3
import re
from utils.state import Rass, City, Admin, Area, Item, Gram, Balance, Balance_del, Clad
import logging
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

async def admin_balance_menu(call: CallbackQuery, bot: Bot):
    try:
        key_item = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Добавить Баланс", callback_data='add_balance_set_')],
            [InlineKeyboardButton(text="Удалить Баланс", callback_data='del_balance_set_')],
            [InlineKeyboardButton(text="Просмотр Баланса", callback_data='show_balance_set_')],
            [InlineKeyboardButton(text="Назад", callback_data='admin_command')]

        ])

        await bot.send_message(call.message.chat.id, "Выберите действие.", reply_markup=key_item)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

async def add_balance_set(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id
        await bot.send_message(user_id, f"Введите external_id пользователя:")
        await bot.delete_message(user_id, call.message.message_id)
        await state.set_state(Balance.external_id)
    except:
        pass

async def add_balance_end(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        external_id = message.text
        await bot.delete_message(user_id, message.message_id - 1)
        await state.update_data(external_id=external_id)
        await bot.send_message(user_id, f"Введите сумму которую хотите добавить пользователю {external_id}:")
        await state.set_state(Balance.balance_summ)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_balance_ex_end(message: Message, bot: Bot, state: FSMContext):
    try:
        balance = message.text
        user_id = message.chat.id
        context_data = await state.get_data()
        external_i = context_data.get('external_id')
        external_id = str(external_i)
        await bot.delete_message(user_id, message.message_id - 1)

        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()

        cursor.execute("SELECT balance FROM users_shop WHERE external_id = ?", (external_id,))

        current_balance = cursor.fetchone()

        conn.close()
        if current_balance is not None:
            current_balance = int(current_balance[0])
            balances = int(balance)
            new_balance = current_balance + balances  # Добавление суммы к текущему балансу
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE users_shop SET balance = ? WHERE external_id = ?", (new_balance, external_id))
            conn.commit()
            conn.close()
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])
            await bot.send_message(user_id, f"Баланс для external_id {external_id} был успешно обновлен.\n "
                                            f"Новый баланс: {new_balance}",
                                   reply_markup=key_item)
            await bot.delete_message(user_id, message.message_id)
        else:

            key_item = InlineKeyboardMarkup(inline_keyboard=[

                [InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')], ])

            await bot.send_message(user_id, f"Баланс для external_id {external_id} не найден."
                                   , reply_markup=key_item)
            await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def del_balance_set(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id
        await bot.send_message(user_id, f"Введите external_id пользователя:")
        await state.set_state(Balance_del.external_id_del)
        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass

async def del_balance_end(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        external_id = message.text
        await bot.delete_message(user_id, message.message_id - 1)
        await state.update_data(external_id=external_id)

        await bot.send_message(user_id, f"Введите сумму которую хотите добавить пользователю {external_id}:")
        await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def del_balance_ex_end(message: Message, bot: Bot, state: FSMContext):
    try:
        balance = message.text
        user_id = message.chat.id
        context_data = await state.get_data()
        external_i = context_data.get('external_id')
        external_id = str(external_i)
        await bot.delete_message(user_id, message.message_id - 1)

        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()

        cursor.execute("SELECT balance FROM users_shop WHERE external_id = ?", (external_id,))

        current_balance = cursor.fetchone()

        conn.close()
        if current_balance is not None:
            current_balance = int(current_balance[0])
            balances = int(balance)
            new_balance = current_balance - balances
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE users_shop SET balance = ? WHERE external_id = ?", (new_balance, external_id))
            conn.commit()
            conn.close()
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])
            await bot.send_message(user_id, f"Баланс для external_id {external_id} был успешно обновлен.\n "
                                            f"Новый баланс: {new_balance}",
                                   reply_markup=key_item)
            await bot.delete_message(user_id, message.message_id)

        else:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])
            await bot.send_message(user_id, f"Баланс для external_id {external_id} не найден."
                                   , reply_markup=key_item)
            await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def show_balance(call: CallbackQuery, bot: Bot):
    try:
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT external_id, balance FROM users_shop")
        balances = cursor.fetchall()
        conn.close()
        key_item = InlineKeyboardMarkup(inline_keyboard=[

            [InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')], ])

        if balances:
            message_text = "Список Баланса Пользователей:\n"
            for balance in balances:
                external_id, user_balance = balance
                message_text += f"External ID: {external_id}\n"
                message_text += f"Баланс: {user_balance}\n\n"

            await bot.send_message(call.message.chat.id, message_text, reply_markup=key_item)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        else:
            await bot.send_message(call.message.chat.id, "Баланс пользователей не найден.", reply_markup=key_item)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

