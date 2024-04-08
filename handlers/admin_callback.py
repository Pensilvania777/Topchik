from aiogram import Bot
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
import sqlite3
import re
from utils.state import Rass, City, Admin, Area, Item, Gram, Balance, Balance_del, Clad
import logging
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta







async def confirm_blik(call: CallbackQuery, bot: Bot):
    try:
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cheker_conf")
        ex_id = cursor.fetchall()
        conn.close()
        if ex_id:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text=ex_ids[2],
                                         callback_data=f'_blik_confirm_{ex_ids[2]}') for ex_ids in ex_id
                ]
            ])

            await bot.send_message(call.message.chat.id, "Выберите external_id чтоб посмотреть его чек.",
                                   reply_markup=key_item)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        else:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])
            await bot.send_message(call.message.chat.id, "У вас нет чеков.", reply_markup=key_item)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

async def confirm_blik_mid(call: CallbackQuery, bot: Bot):
    try:
        ex_id = call.data.split('_')[3]
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cheker_conf WHERE external_id=?", (ex_id,))
        check = cursor.fetchall()
        conn.close()
        print(check)
        if check:
            id_check, number_check, external_id, name_user, price, photo_check = check[0]
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Подтвердить ✅",
                                         callback_data=f'blik_okey_{ex_id}_{price}_{id_check}'),
                    InlineKeyboardButton(text="Удалить 🗑", callback_data=f'blik_delete_{id_check}')
                ],
                [
                    InlineKeyboardButton(text="Назад", callback_data='admin_check')
                ]
            ])
            await bot.send_photo(call.message.chat.id, photo_check, caption=f"ID_чека{id_check}\n"
                                                                            f"Номер чека: #{number_check}\n"
                                                                            f"ID_пользователя: {external_id}\n"
                                                                            f"Имя пользователя: {name_user}\n"
                                                                            f"Сумма чека: {price} zl\n"
                                 , reply_markup=key_item)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        else:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Назад", callback_data='admin_check')
                ]
            ])
            await bot.send_message(call.message.chat.id, "Выберите external_id чтоб посмотреть его чек.",
                                   reply_markup=key_item)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

async def confirm_blik_end(call: CallbackQuery, bot: Bot):
    try:
        ex_id = call.data.split('_')[2]
        price = call.data.split('_')[3]
        id_check = call.data.split('_')[4]
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users_shop WHERE external_id=?", (ex_id,))
        balance = cursor.fetchone()
        conn.close()
        key_item = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Меню", callback_data='admin_command')
            ]
        ])

        if balance:
            bal = int(balance[0])
            pri = int(price)
            summ = pri + bal
            print(summ)
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()

            cursor.execute("UPDATE users_shop SET balance=? WHERE external_id=?", (summ, ex_id))

            conn.commit()
            conn.close()
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()

            cursor.execute("DELETE FROM cheker_conf WHERE id=?", (id_check,))

            conn.commit()
            conn.close()

            await bot.send_message(call.message.chat.id,
                                   f"Баланс пользователя {ex_id}\n Пополнен на {price}\n Обновленный баланс {summ}",
                                   reply_markup=key_item)
            await bot.delete_message(call.message.chat.id, call.message.message_id)

        else:
            await bot.send_message(call.message.chat.id,
                                   f"Баланс пользователя {ex_id} не найден.",
                                   reply_markup=key_item)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

async def delete_blick_end(call: CallbackQuery, bot: Bot):
    try:
        id_check = call.data.split('_')[2]
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM cheker_conf WHERE id=?", (id_check,))

        conn.commit()
        conn.close()

        key_item = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Меню", callback_data='admin_command')
            ]
        ])

        await bot.send_message(call.message.chat.id,
                               f"Чек удален (id = {id_check})",
                               reply_markup=key_item)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
