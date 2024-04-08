from aiogram import Bot
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
import sqlite3
import re
from utils.state import Rass, City, Admin, Area, Item, Gram, Balance, Balance_del, Clad
import logging
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta


async def admin_message_true(call: CallbackQuery, state: FSMContext, bot: Bot):
    try:
        await call.message.answer("Введите текст для рассылки:")
        await state.set_state(Rass.rass_text)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass


async def admin_message_photo(message: Message, state: FSMContext, bot: Bot):
    try:
        await bot.delete_message(message.chat.id, message.message_id - 1)

        await message.answer("Отправьте фото для рассылки :")
        await state.update_data(rass_text=message.text)
        await bot.delete_message(message.chat.id, message.message_id)
        await state.set_state(Rass.rass_photo)
    except:
        pass


async def admin_message_end(message: Message, bot: Bot, state: FSMContext):
    try:
        key = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Меню 💫️", callback_data='back_menu_st')
            ]
        ])

        await state.update_data(rass_photo=message.photo[-1].file_id)
        await state.set_state(Rass.rass_photo)
        await bot.send_message(message.chat.id, "Рассылка завершена.", reply_markup=key)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Удалить 🗑️", callback_data='mess_del')
            ]
        ])
        await bot.delete_message(message.chat.id, message.message_id - 1)

        context_data = await state.get_data()

        rass_text = context_data.get('rass_text')
        rass_photo = context_data.get('rass_photo')
        text = str(rass_text)
        if rass_photo:
            photo_url = message.photo[-1].file_id
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute("SELECT external_id FROM users_shop")
            user_ids = cursor.fetchall()
            conn.close()

            for user_id in user_ids:
                try:
                    await bot.send_photo(user_id[0], rass_photo, caption=text, reply_markup=keyboard)
                    await bot.delete_message(message.chat.id, message.message_id)

                except Exception as e:
                    print(f"Failed to send message to user {user_id[0]} with error: {e}")
        else:
            photo_url = None
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute("SELECT external_id FROM users_shop")
            user_ids = cursor.fetchall()
            conn.close()

            for user_id in user_ids:
                try:
                    await bot.send_message(user_id[0], text, reply_markup=keyboard)
                    await bot.delete_message(message.chat.id, message.message_id)
                except Exception as e:
                    print(f"Failed to send message to user {user_id[0]} with error: {e}")
    except:
        pass

