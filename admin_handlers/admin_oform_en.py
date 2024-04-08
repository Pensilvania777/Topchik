from aiogram import Bot
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
import sqlite3
import re
from utils.state import Rass, City, Admin, Area, Item, Gram, Balance, Balance_del, Clad
import logging
from utils.state import oform_en
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

async def oform_start_menu_en(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления Главного меню:")
        await state.set_state(oform_en.text_menu)

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass

async def add_oform_photo_menu_en(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_menu=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления Главного меню:")
        await state.set_state(oform_en.photo_menu)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def add_oform_menu_end_en(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_menu = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_menu = context_data.get('text_menu')
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_en WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_en SET text_menu = ?, photo_menu = ? WHERE id = ?''',
                           (text_menu, photo_menu, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_en (id, text_menu, photo_menu) VALUES (?, ?, ?)''', (photo_id ,text_menu, photo_menu))
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

async def oform_start_city_en(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления Города:")
        await state.set_state(oform_en.text_city)

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass

async def add_oform_photo_city_en(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_city=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления Города:")
        await state.set_state(oform_en.photo_city)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def add_oform_city_end_en(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_city = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_city = context_data.get('text_city')
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_en WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_en SET text_city = ?, photo_city = ? WHERE id = ?''',
                           (text_city, photo_city, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_en (id, text_city, photo_city) VALUES (?, ?, ?)''', (photo_id ,text_city, photo_city))
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

async def oform_start_area_en(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления Района:")
        await state.set_state(oform_en.text_area)

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass

async def add_oform_photo_area_en(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_area=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления Района:")
        await state.set_state(oform_en.photo_area)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def add_oform_area_end_en(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_area = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_area = context_data.get('text_area')
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_en WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_en SET text_area = ?, photo_area = ? WHERE id = ?''',
                           (text_area, photo_area, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_en (id, text_area, photo_area) VALUES (?, ?, ?)''',
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

async def oform_start_language_en(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления языка:")
        await state.set_state(oform_en.text_language)

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass

async def add_oform_photo_language_en(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_language=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления языка:")
        await state.set_state(oform_en.photo_language)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def add_oform_language_end_en(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_language = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_language = context_data.get('text_language')
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_en WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_en SET text_language = ?, photo_language = ? WHERE id = ?''',
                           (text_language, photo_language, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_en (id, text_language, photo_language) VALUES (?, ?, ?)''', (photo_id ,text_language, photo_language))
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


async def oform_start_instuction_en(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления Инструкции:")
        await state.set_state(oform_en.text_instruction)

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass

async def add_oform_photo_instuction_en(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_instruction=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления Инструкции:")
        await state.set_state(oform_en.photo_instruction)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def add_oform_instruction_end_en(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_instruction = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_instruction = context_data.get('text_instruction')
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_en WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_en SET text_instuction = ?, photo_instruction = ? WHERE id = ?''',
                           (text_instruction, photo_instruction, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_en (id, text_instuction, photo_instruction) VALUES (?, ?, ?)''', (photo_id ,text_instruction, photo_instruction))
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


async def oform_start_rules_en(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления Правил:")
        await state.set_state(oform_en.text_rules)

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass

async def add_oform_photo_rules_en(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_rules=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления Правила:")
        await state.set_state(oform_en.photo_rules)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def add_oform_rules_end_en(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_rules = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_rules = context_data.get('text_rules')
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_en WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_en SET text_rules = ?, photo_rules = ? WHERE id = ?''',
                           (text_rules, photo_rules, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_en (id, text_instruction, photo_instruction) VALUES (?, ?, ?)''',
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



async def oform_start_item_en(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления Товара:")
        await state.set_state(oform_en.text_item)

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def add_oform_photo_item_en(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_item=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления Товара:")
        await state.set_state(oform_en.photo_item)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_oform_item_end_en(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_item = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_item = context_data.get('text_item')
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_en WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_en SET text_item = ?, photo_item = ? WHERE id = ?''',
                           (text_item, photo_item, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_en (id, text_item, photo_item) VALUES (?, ?, ?)''',
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

async def add_oform_photo_profile_en(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте фотографию для оформления Профиля:")
        await state.set_state(oform_en.photo_profile)

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def add_oform_profile_end_en(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_profile = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_en WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_en SET photo_profile = ? WHERE id = ?''',
                           (photo_profile, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_en (id, photo_profile) VALUES (?, ?)''',
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

async def oform_start_actcheck_en(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления Активных чеков:")
        await state.set_state(oform_en.text_actcheck)

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def add_oform_photo_actcheck_en(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_actcheck=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления Активных чеков:")
        await state.set_state(oform_en.photo_actcheck)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_oform_actcheck_end_en(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_item = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_item = context_data.get('text_actcheck')
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_en WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_en SET text_actcheck = ?, photo_actcheck = ? WHERE id = ?''',
                           (text_item, photo_item, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_en (id, text_actcheck, photo_actcheck) VALUES (?, ?, ?)''',
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

async def oform_start_crypto_en(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления Крипто:")
        await state.set_state(oform_en.text_crypto)

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def add_oform_photo_crypto_en(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_crypto=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления Крипто:")
        await state.set_state(oform_en.photo_crypto)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_oform_crypto_end_en(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_item = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_item = context_data.get('text_crypto')
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_en WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_en SET text_crypto = ?, photo_crypto = ? WHERE id = ?''',
                           (text_item, photo_item, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_en (id, text_crypto, photo_crypto) VALUES (?, ?, ?)''',
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

async def oform_start_blikwplata_en(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id
        print("GEYr")

        await bot.send_message(user_id, "Отправьте текст для оформления Blik wplata:")
        await state.set_state(oform_en.text_blik_wplata)

        await bot.delete_message(user_id, call.message.message_id)
    except Exception as e:
        print(e)


async def add_oform_photo_blikwplata_en(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_blikwplata=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления Blik wplata:")
        await state.set_state(oform_en.photo_blik_wplata)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_oform_end_en_blik(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_item = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_item = context_data.get('text_blikwplata')
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        print("FOTO", photo_item)
        cursor.execute('''SELECT COUNT(*) FROM oform_en WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_en SET text_blick_wplata = ?, photo_blick_wplata = ? WHERE id = ?''',
                           (text_item, photo_item, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_en (id, text_blick_wplata, photo_blick_wplata) VALUES (?, ?, ?)''',
                           (photo_id, text_item, photo_item))
            print("Запись добавлена")
        conn.commit()
        conn.close()

        key_menu = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_oform_menu_add')
            ]
        ])
        await bot.send_photo(user_id, photo_item, caption="Оформление Blik wplata DASDSAдобавлено\n"
                                                           f"Текст: {text_item}",
                             reply_markup=key_menu)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def oform_start_banc_en(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления Баланса:")
        await state.set_state(oform_en.text_banc)

        await bot.delete_message(user_id, call.message.message_id)
    except Exception as e:
        print(e)


async def add_oform_photo_banc_en(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_banc=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления Баланса:")
        await state.set_state(oform_en.photo_banc)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_oform_banc_end_en(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_item = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_item = context_data.get('text_banc')
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_en WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_en SET text_banc = ?, photo_banc = ? WHERE id = ?''',
                           (text_item, photo_item, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_en (id, text_banc, photo_banc) VALUES (?, ?, ?)''',
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


async def oform_start_izbpokup_en(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления Избранных покупок:")
        await state.set_state(oform_en.text_izbpokup)

        await bot.delete_message(user_id, call.message.message_id)
    except Exception as e:
        print(e)


async def add_oform_photo_izbpokup_en(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_izbpokup=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления Избранных покупок:")
        await state.set_state(oform_en.photo_izbpokup)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_oform_izbpokup_end_en(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_item = message.photo[-1].file_id
        user_id = message.chat.id

        await bot.delete_message(user_id, message.message_id - 1)

        context_data = await state.get_data()
        text_item = context_data.get('text_izbpokup')
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        photo_id = 1
        cursor.execute('''SELECT COUNT(*) FROM oform_en WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_en SET text_izbpokup = ?, photo_izbpokup = ? WHERE id = ?''',
                           (text_item, photo_item, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_en (id, text_izbpokup, photo_izbpokup) VALUES (?, ?, ?)''',
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


async def oform_start_reff_en(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id

        await bot.send_message(user_id, "Отправьте текст для оформления Реферальной системы:")
        await state.set_state(oform_en.text_reff)

        await bot.delete_message(user_id, call.message.message_id)
    except Exception as e:
        print(e)


async def add_oform_photo_reff_en(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        await state.update_data(text_reff=message.text)
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, "Отправьте фотографию для оформления Реферальной программы:")
        await state.set_state(oform_en.photo_reff)

        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_oform_reff_end_en(message: Message, bot: Bot, state: FSMContext):
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
        cursor.execute('''SELECT COUNT(*) FROM oform_en WHERE id = ?''', (photo_id,))
        existing_record_count = cursor.fetchone()[0]
        if existing_record_count > 0:
            cursor.execute('''UPDATE oform_en SET text_reff = ?, photo_reff = ? WHERE id = ?''',
                           (text_item, photo_item, photo_id))
            print("Запись обновлена")
        else:
            cursor.execute('''INSERT INTO oform_en (id, text_reff, photo_reff) VALUES (?, ?, ?)''',
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





