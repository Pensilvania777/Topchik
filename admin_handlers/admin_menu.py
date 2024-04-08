from aiogram import Bot
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
import sqlite3
import re
from utils.state import Rass, City, Admin, Area, Item, Gram, Balance, Balance_del, Clad
import logging
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta


async def admin_handler(message: Message, bot: Bot):
    try:
        user_external_id = message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()

        # Выполняем SQL-запрос для проверки наличия пользователя с заданным external_id в таблице админов
        cursor.execute('SELECT external_admin FROM admin WHERE external_admin = ?', (user_external_id,))
        admin = cursor.fetchone()

        # Закрываем соединение с базой данных
        conn.close()

        if admin is not None:
            admin_str = admin[0]

            # Используем регулярное выражение для удаления всех символов, кроме цифр
            digits_only = re.sub(r'\D', '', admin_str)

            # Преобразуем user_external_id в строку, чтобы сравнить с digits_only
            user_external_id_str = str(user_external_id)

            if digits_only == user_external_id_str:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[

                    [
                        InlineKeyboardButton(text="Город", callback_data='admin_city'),
                        InlineKeyboardButton(text="Район", callback_data='admin_area')
                    ],
                    [
                        InlineKeyboardButton(text="Товар", callback_data='admin_item'),
                        InlineKeyboardButton(text="Фасовка", callback_data='admin_gram')
                    ],
                    [
                        InlineKeyboardButton(text="Клады", callback_data='admin_clad'),
                        InlineKeyboardButton(text="Чеки BLIK", callback_data='admin_check')
                    ],
                    [
                        InlineKeyboardButton(text="Админ", callback_data='admin_setting'),
                        InlineKeyboardButton(text="Баланс", callback_data='admin_balance')
                    ],
                    [
                        InlineKeyboardButton(text="Рассылка", callback_data='admin_message'),
                        InlineKeyboardButton(text="Аналитика ", callback_data='admin_analis')
                    ],
                    [
                        InlineKeyboardButton(text="Кладмэн", callback_data='cladman_'),
                    ],
                    [
                        InlineKeyboardButton(text="Оформление", callback_data='oform_'),
                    ],
                    [
                        InlineKeyboardButton(text="Выйти в меню", callback_data='back_menu_st_')
                    ]
                ])
                await bot.send_message(message.chat.id, "Добро пожаловать в админ панель!", reply_markup=keyboard)

            else:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Вернуться в меню", callback_data='main_menu')
                    ]
                ])
                await bot.send_message(message.chat.id, "У вас нет доступа для админ панели!", reply_markup=keyboard)
    except:
        pass

async def admin_return_menu(call: CallbackQuery, bot: Bot):
    try:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[

            [
                InlineKeyboardButton(text="Город", callback_data='admin_city'),
                InlineKeyboardButton(text="Район", callback_data='admin_area')
            ],
            [
                InlineKeyboardButton(text="Товар", callback_data='admin_item'),
                InlineKeyboardButton(text="Фасовка", callback_data='admin_gram')
            ],
            [
                InlineKeyboardButton(text="Клады", callback_data='admin_clad'),
                InlineKeyboardButton(text="Чеки BLIK", callback_data='admin_check')
            ],
            [
                InlineKeyboardButton(text="Админ", callback_data='admin_setting'),
                InlineKeyboardButton(text="Баланс", callback_data='admin_balance')
            ],
            [
                InlineKeyboardButton(text="Рассылка", callback_data='admin_message'),
                InlineKeyboardButton(text="Аналитика ", callback_data='admin_analis')
            ],
            [
                InlineKeyboardButton(text="Кладмэн", callback_data='cladman_'),
            ],
            [
                InlineKeyboardButton(text="Оформление", callback_data='oform_'),
            ],
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='back_menu_st_')
            ]
        ])
        await bot.send_message(call.message.chat.id, "Добро пожаловать в админ панель!", reply_markup=keyboard)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass