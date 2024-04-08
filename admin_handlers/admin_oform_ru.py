from aiogram import Bot
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
import sqlite3
import re
from utils.state import Rass, City, Admin, Area, Item, Gram, Balance, Balance_del, Clad
import logging
from utils.state import oform_ru
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

async def oform_start_menu(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления Главного меню:")
        await state.set_state(oform_ru.text_menu)

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass

async def add_oform_photo_menu(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_menu=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления Главного меню:")
        await state.set_state(oform_ru.photo_menu)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def add_oform_menu_end(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_menu = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_menu = context_data.get('text_menu')
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_ru WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_ru SET text_menu = ?, photo_menu = ? WHERE id = ?''',
                           (text_menu, photo_menu, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_ru (id, text_menu, photo_menu) VALUES (?, ?, ?)''', (photo_id ,text_menu, photo_menu))
            print("Запись добавлена")
        conn.commit()
        conn.close()

        key_menu = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_oform_menu_add')
            ]
        ])
        await bot.send_photo(user_id, photo_menu, caption="Главное меню добавлено\n"
                                                          f"Текст: {text_menu}",
                             reply_markup=key_menu)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def oform_start_city(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления Города:")
        await state.set_state(oform_ru.text_city)

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass

async def add_oform_photo_city(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_city=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления Города:")
        await state.set_state(oform_ru.photo_city)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def add_oform_city_end(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_city = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_city = context_data.get('text_city')
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_ru WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_ru SET text_city = ?, photo_city = ? WHERE id = ?''',
                           (text_city, photo_city, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_ru (id, text_city, photo_city) VALUES (?, ?, ?)''', (photo_id ,text_city, photo_city))
            print("Запись добавлена")
        conn.commit()
        conn.close()

        key_menu = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_oform_menu_add')
            ]
        ])
        await bot.send_photo(user_id, photo_city, caption="Главное меню добавлено\n"
                                                          f"Текст: {text_city}",
                             reply_markup=key_menu)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def oform_start_area(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления Района:")
        await state.set_state(oform_ru.text_area)

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass

async def add_oform_photo_area(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_area=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления Района:")
        await state.set_state(oform_ru.photo_area)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def add_oform_area_end(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_area = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_area = context_data.get('text_area')
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_ru WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_ru SET text_area = ?, photo_area = ? WHERE id = ?''',
                           (text_area, photo_area, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_ru (id, text_area, photo_area) VALUES (?, ?, ?)''',
                           (photo_id ,text_area, photo_area))
            print("Запись добавлена")
        conn.commit()
        conn.close()

        key_menu = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_oform_menu_add')
            ]
        ])
        await bot.send_photo(user_id, photo_area, caption="Главное меню добавлено\n"
                                                          f"Текст: {text_area}",
                             reply_markup=key_menu)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def oform_start_language(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления языка:")
        await state.set_state(oform_ru.text_language)

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass

async def add_oform_photo_language(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_language=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления языка:")
        await state.set_state(oform_ru.photo_language)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def add_oform_language_end(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_language = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_language = context_data.get('text_language')
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_ru WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_ru SET text_language = ?, photo_language = ? WHERE id = ?''',
                           (text_language, photo_language, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_ru (id, text_language, photo_language) VALUES (?, ?, ?)''', (photo_id ,text_language, photo_language))
            print("Запись добавлена")
        conn.commit()
        conn.close()

        key_menu = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_oform_menu_add')
            ]
        ])
        await bot.send_photo(user_id, photo_language, caption="Главное меню добавлено\n"
                                                          f"Текст: {text_language}",
                             reply_markup=key_menu)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def oform_start_instuction(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления Инструкции:")
        await state.set_state(oform_ru.text_instruction)

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass

async def add_oform_photo_instuction(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_instruction=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления Инструкции:")
        await state.set_state(oform_ru.photo_instruction)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def add_oform_instruction_end(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_instruction = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_instruction = context_data.get('text_instruction')
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_ru WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_ru SET text_instuction = ?, photo_instruction = ? WHERE id = ?''',
                           (text_instruction, photo_instruction, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_ru (id, text_instuction, photo_instruction) VALUES (?, ?, ?)''', (photo_id ,text_instruction, photo_instruction))
            print("Запись добавлена")
        conn.commit()
        conn.close()

        key_menu = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_oform_menu_add')
            ]
        ])
        await bot.send_photo(user_id, photo_instruction, caption="Инструкция добавлено\n"
                                                          f"Текст: {text_instruction}",
                             reply_markup=key_menu)

        await bot.delete_message(user_id, message.message_id)
    except Exception as e:
        print(repr(e))


async def oform_start_rules(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления Правил:")
        await state.set_state(oform_ru.text_rules)

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass

async def add_oform_photo_rules(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_rules=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления Правила:")
        await state.set_state(oform_ru.photo_rules)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def add_oform_rules_end(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_rules = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_rules = context_data.get('text_rules')
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_ru WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_ru SET text_rules = ?, photo_rules = ? WHERE id = ?''',
                           (text_rules, photo_rules, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_ru (id, text_instruction, photo_instruction) VALUES (?, ?, ?)''',
                           (photo_id ,text_rules, photo_rules))
            print("Запись добавлена")
        conn.commit()
        conn.close()

        key_menu = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_oform_menu_add')
            ]
        ])
        await bot.send_photo(user_id, photo_rules, caption="Правила добавлены\n"
                                                          f"Текст: {text_rules}",
                             reply_markup=key_menu)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass



async def oform_start_item(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления Товара:")
        await state.set_state(oform_ru.text_item)

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def add_oform_photo_item(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_item=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления Товара:")
        await state.set_state(oform_ru.photo_item)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_oform_item_end(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_item = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_item = context_data.get('text_item')
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_ru WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_ru SET text_item = ?, photo_item = ? WHERE id = ?''',
                           (text_item, photo_item, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_ru (id, text_item, photo_item) VALUES (?, ?, ?)''',
                           (photo_id, text_item, photo_item))
            print("Запись добавлена")
        conn.commit()
        conn.close()

        key_menu = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_oform_menu_add')
            ]
        ])
        await bot.send_photo(user_id, photo_item, caption="Оформление товара добавлено\n"
                                                           f"Текст: {text_item}",
                             reply_markup=key_menu)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def add_oform_photo_profile(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте фотографию для оформления Профиля:")
        await state.set_state(oform_ru.photo_profile)

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def add_oform_profile_end(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_profile = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_ru WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_ru SET photo_profile = ? WHERE id = ?''',
                           (photo_profile, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_ru (id, photo_profile) VALUES (?, ?)''',
                           (photo_id, photo_profile))
            print("Запись добавлена")
        conn.commit()
        conn.close()

        key_menu = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_oform_menu_add')
            ]
        ])
        await bot.send_photo(user_id, photo_profile, caption="Оформление Профиля добавлено\n",
                             reply_markup=key_menu)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def oform_start_actcheck(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления Активных чеков:")
        await state.set_state(oform_ru.text_actcheck)

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def add_oform_photo_actcheck(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_actcheck=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления Активных чеков:")
        await state.set_state(oform_ru.photo_actcheck)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_oform_actcheck_end(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_item = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_item = context_data.get('text_actcheck')
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_ru WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_ru SET text_actcheck = ?, photo_actcheck = ? WHERE id = ?''',
                           (text_item, photo_item, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_ru (id, text_actcheck, photo_actcheck) VALUES (?, ?, ?)''',
                           (photo_id, text_item, photo_item))
            print("Запись добавлена")
        conn.commit()
        conn.close()

        key_menu = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_oform_menu_add')
            ]
        ])
        await bot.send_photo(user_id, photo_item, caption="Оформление Активных чеков добавлено\n"
                                                           f"Текст: {text_item}",
                             reply_markup=key_menu)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def oform_start_crypto(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления Крипто:")
        await state.set_state(oform_ru.text_crypto)

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def add_oform_photo_crypto(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_crypto=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления Крипто:")
        await state.set_state(oform_ru.photo_crypto)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_oform_crypto_end(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_item = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_item = context_data.get('text_crypto')
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_ru WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_ru SET text_crypto = ?, photo_crypto = ? WHERE id = ?''',
                           (text_item, photo_item, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_ru (id, text_crypto, photo_crypto) VALUES (?, ?, ?)''',
                           (photo_id, text_item, photo_item))
            print("Запись добавлена")
        conn.commit()
        conn.close()

        key_menu = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_oform_menu_add')
            ]
        ])
        await bot.send_photo(user_id, photo_item, caption="Оформление Крипты добавлено\n"
                                                           f"Текст: {text_item}",
                             reply_markup=key_menu)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def oform_start_blikwplata(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления Blik wplata:")
        await state.set_state(oform_ru.text_blik_wplata)

        await bot.delete_message(user_id, call.message.message_id)
    except Exception as e:
        print(e)


async def add_oform_photo_blikwplata(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_blikwplata=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления Blik wplata:")
        await state.set_state(oform_ru.photo_blik_wplata)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_oform_blickwplata_end(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_item = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_item = context_data.get('text_blikwplata')
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_ru WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_ru SET text_blick_wplata = ?, photo_blick_wplata = ? WHERE id = ?''',
                           (text_item, photo_item, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_ru (id, text_blick_wplata, photo_blick_wplata) VALUES (?, ?, ?)''',
                           (photo_id, text_item, photo_item))
            print("Запись добавлена")
        conn.commit()
        conn.close()

        key_menu = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_oform_menu_add')
            ]
        ])
        await bot.send_photo(user_id, photo_item, caption="Оформление Blik wplata добавлено\n"
                                                           f"Текст: {text_item}",
                             reply_markup=key_menu)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def oform_start_banc(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления Баланса:")
        await state.set_state(oform_ru.text_banc)

        await bot.delete_message(user_id, call.message.message_id)
    except Exception as e:
        print(e)


async def add_oform_photo_banc(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_banc=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления Баланса:")
        await state.set_state(oform_ru.photo_banc)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_oform_banc_end(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_item = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_item = context_data.get('text_banc')
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_ru WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_ru SET text_banc = ?, photo_banc = ? WHERE id = ?''',
                           (text_item, photo_item, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_ru (id, text_banc, photo_banc) VALUES (?, ?, ?)''',
                           (photo_id, text_item, photo_item))
            print("Запись добавлена")
        conn.commit()
        conn.close()

        key_menu = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_oform_menu_add')
            ]
        ])
        await bot.send_photo(user_id, photo_item, caption="Оформление Баланса добавлено\n"
                                                           f"Текст: {text_item}",
                             reply_markup=key_menu)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def oform_start_izbpokup(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления Избранных покупок:")
        await state.set_state(oform_ru.text_izbpokup)

        await bot.delete_message(user_id, call.message.message_id)
    except Exception as e:
        print(e)


async def add_oform_photo_izbpokup(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_izbpokup=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления Избранных покупок:")
        await state.set_state(oform_ru.photo_izbpokup)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_oform_izbpokup_end(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_item = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_item = context_data.get('text_izbpokup')
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_ru WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_ru SET text_izbpokup = ?, photo_izbpokup = ? WHERE id = ?''',
                           (text_item, photo_item, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_ru (id, text_izbpokup, photo_izbpokup) VALUES (?, ?, ?)''',
                           (photo_id, text_item, photo_item))
            print("Запись добавлена")
        conn.commit()
        conn.close()

        key_menu = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_oform_menu_add')
            ]
        ])
        await bot.send_photo(user_id, photo_item, caption="Оформление Избранных покупок добавлено\n"
                                                           f"Текст: {text_item}",
                             reply_markup=key_menu)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def oform_start_reff(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления Реферальной системы:")
        await state.set_state(oform_ru.text_reff)

        await bot.delete_message(user_id, call.message.message_id)
    except Exception as e:
        print(e)


async def add_oform_photo_reff(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_reff=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления Реферальной программы:")
        await state.set_state(oform_ru.photo_reff)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_oform_reff_end(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_item = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_item = context_data.get('text_reff')
        print(text_item)
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_ru WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_ru SET text_reff = ?, photo_reff = ? WHERE id = ?''',
                           (text_item, photo_item, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_ru (id, text_reff, photo_reff) VALUES (?, ?, ?)''',
                           (photo_id, text_item, photo_item))
            print("Запись добавлена")
        conn.commit()
        conn.close()

        key_menu = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_oform_menu_add')
            ]
        ])
        await bot.send_photo(user_id, photo_item, caption="Оформление Реферальной системы добавлено\n"
                                                           f"Текст: {text_item}",
                             reply_markup=key_menu)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass






async def add_oform_iban(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления Номер счета:")
        await state.set_state(oform_ru.text_iban)

        await bot.delete_message(user_id, call.message.message_id)
    except Exception as e:
        print(e)

async def add_oform_number_phone(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_iban=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте тест для оформления Номера телефона:")
        await state.set_state(oform_ru.text_number_phone)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_oform_name_blik(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_number_phone=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте текст для оформления Имя получателя:")
        await state.set_state(oform_ru.text_name_poluch)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_oform_blick_end(message: Message, bot: Bot, state: FSMContext):
    try:
        name = message.text
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_iban = context_data.get('text_iban')
        text_number_phone = context_data.get('text_number_phone')

        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO blik (text_iban, text_number_phone, text_nameuser) VALUES (?, ?, ?)''',
                       (text_iban, text_number_phone, name))
        print("Запись обновлена")

        conn.commit()
        conn.close()

        key_menu = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_oform_menu_add')
            ]
        ])
        await bot.send_message(user_id, "Оформление Blik добавлено\n", reply_markup=key_menu)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass