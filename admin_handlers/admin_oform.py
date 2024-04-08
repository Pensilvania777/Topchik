from aiogram import Bot
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
import sqlite3
import re
from utils.state import Rass, City, Admin, Area, Item, Gram, Balance, Balance_del, Clad
import logging
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta


async def ofor_menu(call: CallbackQuery, bot: Bot):
    try:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Добавить оформление",
                                     callback_data='admin_oform_menu_add')
            ],
            [
                InlineKeyboardButton(text="Вернуться в меню",
                                     callback_data='admin_menu')
            ]
        ])
        await bot.send_message(call.message.chat.id, "Оформление\n"
                                                "Выберите действие:", reply_markup=keyboard)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(repr(e))


async def ofor_laguange_add(call: CallbackQuery, bot: Bot):
    try:
        ru = "ru"
        en = "en"
        keyboard = InlineKeyboardMarkup(inline_keyboard=[

            [
                InlineKeyboardButton(text="Русский",
                                     callback_data=f'admin_language_{ru}'),
                InlineKeyboardButton(text="Английский",
                                     callback_data=f'admin_language_{en}'),
            ],
            [
                InlineKeyboardButton(text="Назад",
                                     callback_data='oform_'),
            ]
        ])
        await bot.send_message(call.message.chat.id, "Оформление\n"
                                                "Выберите действие:", reply_markup=keyboard)
        await bot.delete_message(call.message.chat.id, call.message.message_id)

    except Exception as e:
        print(repr(e))


async def ofor_menu_add(call: CallbackQuery, bot: Bot):
    try:

        launguage = call.data.split('_')[2]
        if launguage == 'ru':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Главное меню",
                                         callback_data=f'admin_oform_go_{launguage}'),
                ],
                [
                    InlineKeyboardButton(text="Баланс",
                                         callback_data=f'admin_oform_balance_{launguage}')
                ],
                [
                    InlineKeyboardButton(text="Назад",
                                         callback_data='admin_oform_menu_add')
                ],
            ])
            await bot.send_message(call.message.chat.id, "Оформление RUS 🇷🇺\n"
                                                         "Выберите действие:", reply_markup=keyboard)
            await bot.delete_message(call.message.chat.id, call.message.message_id)

        elif launguage == 'en':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Главное меню",
                                         callback_data=f'admin_oform_go_{launguage}'),
                ],
                [
                    InlineKeyboardButton(text="Баланс",
                                         callback_data=f'admin_oform_balance_{launguage}')
                ],
                [
                    InlineKeyboardButton(text="Назад",
                                         callback_data='admin_oform_menu_add')
                ],
            ])
            await bot.send_message(call.message.chat.id, "Оформление ENGLISH 🇺🇸\n"
                                                        "Выберите действие:", reply_markup=keyboard)
            await bot.delete_message(call.message.chat.id, call.message.message_id)

    except Exception as e:
        print(repr(e))


async def ofor_menu_add_start(call: CallbackQuery, bot: Bot):
    try:
        launguage = call.data.split('_')[3]
        if launguage == 'ru':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Главное меню",
                                         callback_data=f'admin_oform_start_menu_ru_{launguage}'),
                    InlineKeyboardButton(text="Товар",
                                         callback_data=f'admin_oform_item_ru_')

                ],
                [
                    InlineKeyboardButton(text="Выбор города",
                                         callback_data='admin_oform_city_ru_'),
                    InlineKeyboardButton(text="Выбор района",
                                         callback_data='admin_oform_area_ru_')
                ],
                [
                    InlineKeyboardButton(text="Профиль",
                                         callback_data='admin_oform_profile_ru_'),
                    InlineKeyboardButton(text="Язык",
                                         callback_data='admin_oform_language_ru_')
                ],
                [
                    InlineKeyboardButton(text="Избранные покупки",
                                         callback_data='admin_oform_izbpokup_ru_'),
                    InlineKeyboardButton(text="Реферальная система",
                                         callback_data='admin_oform_reff_ru_')
                ],
                [
                    InlineKeyboardButton(text="Инструкция",
                                         callback_data='admin_oform_instuction_ru_'),
                    InlineKeyboardButton(text="Правила",
                                         callback_data='admin_oform_rules_ru_')
                ],
                [
                    InlineKeyboardButton(text="Назад",
                                         callback_data=f'admin_language_{launguage}')
                ],
            ])
            await bot.send_message(call.message.chat.id, "Оформление RUS 🇷🇺\n"
                                                         "Выберите действие:", reply_markup=keyboard)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        elif launguage == "en":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Главное меню",
                                         callback_data=f'admin_oform_start_menu_en_{launguage}'),
                    InlineKeyboardButton(text="Товар",
                                         callback_data=f'admin_oform_item_en_')

                ],
                [
                    InlineKeyboardButton(text="Выбор города",
                                         callback_data='admin_oform_city_en_'),
                    InlineKeyboardButton(text="Выбор района",
                                         callback_data='admin_oform_area_en_')
                ],
                [
                    InlineKeyboardButton(text="Профиль",
                                         callback_data='admin_oform_profile_en_'),
                    InlineKeyboardButton(text="Язык",
                                         callback_data='admin_oform_language_en_')
                ],
                [
                    InlineKeyboardButton(text="Избранные покупки",
                                         callback_data='admin_oform_izbpokup_en_'),
                    InlineKeyboardButton(text="Реферальная система",
                                         callback_data='admin_oform_reff_en_')
                ],
                [
                    InlineKeyboardButton(text="Инструкция",
                                         callback_data='admin_oform_instuction_en_'),
                    InlineKeyboardButton(text="Правила",
                                         callback_data='admin_oform_rules_en_')
                ],
                [
                    InlineKeyboardButton(text="Назад",
                                         callback_data=f'admin_language_{launguage}')
                ],
            ])
            await bot.send_message(call.message.chat.id, "Оформление EN 🇺🇸\n"
                                                         "Выберите действие:", reply_markup=keyboard)
            await bot.delete_message(call.message.chat.id, call.message.message_id)



    except Exception as e:
        print(repr(e))

async def ofor_balance_add_start(call: CallbackQuery, bot: Bot):
    try:
        launguage = call.data.split('_')[3]
        if launguage == 'ru':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Активные чеки",
                                         callback_data=f'admin_oform_actcheck_ru_{launguage}'),
                    InlineKeyboardButton(text="Баланс",
                                         callback_data=f'admin_oform_banc_ru_{launguage}'),
                ],
                [
                    InlineKeyboardButton(text="Криптовалюта",
                                         callback_data='admin_oform_crypto_ru_'),
                    InlineKeyboardButton(text="BLIK",
                                         callback_data=f'admin_oform_blik_{launguage}')
                ],
                [
                    InlineKeyboardButton(text="Назад",
                                         callback_data=f'admin_language_{launguage}')
                ],
            ])
            await bot.send_message(call.message.chat.id, "Оформление RUS 🇷🇺\n"
                                                         "Выберите действие:", reply_markup=keyboard)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        elif launguage == 'en':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Активные чеки",
                                         callback_data=f'admin_oform_actcheck_en_{launguage}'),
                    InlineKeyboardButton(text="Баланс",
                                         callback_data=f'admin_oform_banc_en_{launguage}'),
                ],
                [
                    InlineKeyboardButton(text="Криптовалюта",
                                         callback_data='admin_oform_crypto_en_'),
                    InlineKeyboardButton(text="BLIK",
                                         callback_data=f'admin_oform_blik_{launguage}')
                ],
                [
                    InlineKeyboardButton(text="Назад",
                                         callback_data=f'admin_language_{launguage}')
                ],
            ])
            await bot.send_message(call.message.chat.id, "Оформление EN 🇺🇸\n"
                                                         "Выберите действие:", reply_markup=keyboard)
            await bot.delete_message(call.message.chat.id, call.message.message_id)

    except Exception as e:
        print(repr(e))

async def ofor_blik_add_start(call: CallbackQuery, bot: Bot):
    try:
        launguage = call.data.split('_')[3]
        if launguage == 'ru':

            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="BLIK по Номеру 📲",
                                         callback_data=f'admin_oform_blik_number_'),
                    InlineKeyboardButton(text="BLIK Wplata 🏦",
                                         callback_data=f'blik_admin_wplata_')
                ],
                [
                    InlineKeyboardButton(text="Назад 🔙",
                                         callback_data=f'admin_oform_balance_{launguage}')
                ]
            ])
            await bot.send_message(call.message.chat.id, "BLIK 📲", reply_markup=keyboard)

        elif launguage == 'en':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="BLIK по Номеру 📲",
                                         callback_data=f'admin_oform_blik_number_'),
                    InlineKeyboardButton(text="BLIK Wplata 🏦",
                                         callback_data=f'wplata_oform_en')
                ],
                [
                    InlineKeyboardButton(text="Назад 🔙",
                                         callback_data=f'admin_oform_balance_{launguage}')
                ]
            ])

            await bot.send_message(call.message.chat.id, "BLIK 📲", reply_markup=keyboard)
        await bot.delete_message(call.message.chat.id, call.message.message_id)

    except Exception as e:
        print(repr(e))

