from aiogram import Bot
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
import sqlite3
import re
from utils.state import Rass, City, Admin, Area, Item, Gram, Balance, Balance_del, Clad
import logging
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

async def admin_clad_menu(call: CallbackQuery, bot: Bot):
    try:
        key_item = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Добавить Клад", callback_data='add_clad_set_')
            ],
            [
                InlineKeyboardButton(text="Удалить Клад", callback_data='del_clad_set_')
            ],
            [
                InlineKeyboardButton(text="Просмотр Кладов", callback_data='show_clad_set_')
            ],
            [
                InlineKeyboardButton(text="Назад", callback_data='admin_command')
            ],
        ])

        await bot.send_message(call.message.chat.id, "Выберите действие.", reply_markup=key_item)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass


async def add_clad(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name_city FROM city")
        items = cursor.fetchall()
        conn.close()

        if len(items) == 0:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')]
            ])
            await bot.send_message(user_id, "Нет доступных Городов", reply_markup=key_item)
            await bot.delete_message(user_id, call.message.message_id)



        else:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text=item[0], callback_data=f'_clad_city_{item[0]}') for item in items
                ],
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])

            await bot.send_message(user_id, f"Выберите Город для добавление клада:", reply_markup=key_item)
            await bot.delete_message(user_id, call.message.message_id)
    except:
        pass

async def add_clad_area(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        city = call.data.split('_')[3]
        await state.update_data(city_clad=city)

        user_id = call.message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name_area FROM area WHERE name_city = ?", (city,))
        items = cursor.fetchall()
        conn.close()

        if len(items) == 0:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])
            await bot.send_message(user_id, "Нет доступных Районов", reply_markup=key_item)
            await bot.delete_message(user_id, call.message.message_id)

        else:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text=item[0], callback_data=f'_clad_area_{city}_{item[0]}') for item in items
                ],
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])
            await bot.send_message(user_id, f"Выберите Район для добавление клада:", reply_markup=key_item)
            await bot.delete_message(user_id, call.message.message_id)
    except:
        pass

async def add_clad_item(call: CallbackQuery, bot: Bot):
    try:
        city = call.data.split('_')[3]
        area = call.data.split('_')[4]

        user_id = call.message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name_item FROM item")
        items = cursor.fetchall()
        conn.close()

        if len(items) == 0:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])

            await bot.send_message(user_id, "Нет доступных Товаров", reply_markup=key_item)
            await bot.delete_message(user_id, call.message.message_id)

        else:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text=item[0],
                                         callback_data=f'_clad_item_{city}_{area}_{item[0]}') for item in items
                ],
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])

            await bot.send_message(user_id, f"Выберите Товар для добавление клада:", reply_markup=key_item)
            await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def add_clad_gram(call: CallbackQuery, bot: Bot):
    try:
        city = call.data.split('_')[3]
        area = call.data.split('_')[4]
        tovar = call.data.split('_')[5]

        user_id = call.message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT gram FROM grams")
        items = cursor.fetchall()
        conn.close()

        if len(items) == 0:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [

                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])

            await bot.send_message(user_id, "Нет доступных Граммовок", reply_markup=key_item)
            await bot.delete_message(user_id, call.message.message_id)

        else:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text=item[0],
                                         callback_data=f'_clad_gram_{city}_{area}_{tovar}_{item[0]}') for item in items
                ],
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])

            await bot.send_message(user_id, f"Выберите Граммовку для добавление клада:", reply_markup=key_item)
            await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def add_clad_grams(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        city = call.data.split('_')[3]
        area = call.data.split('_')[4]
        tovar = call.data.split('_')[5]
        gram = call.data.split('_')[6]
        await state.update_data(area_clad=area)
        await state.update_data(tovar_clad=tovar)
        await state.update_data(gram_clad=gram)

        await state.set_state(Clad.latit)
        user_id = call.message.chat.id
        await bot.send_message(user_id, f"Введите Цену для товара ({tovar}) Граммовка ({gram}):")
        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def add_clad_lat(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        price = message.text

        await state.update_data(price_clad=price)
        await state.set_state(Clad.longtit)

        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, f"Введите Широту Координат (**,******)")
        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_clad_long(message: Message, bot: Bot, state: FSMContext):
    try:
        latitude = message.text
        await state.update_data(latit=latitude)
        await state.set_state(Clad.longdob)

        user_id = message.chat.id
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, f"Введите Долготу Координат (**,******)")
        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_clad_photo(message: Message, bot: Bot, state: FSMContext):
    try:
        longtitude = message.text
        await state.update_data(longtit=longtitude)
        await state.set_state(Clad.photo_clad)

        user_id = message.chat.id
        await bot.delete_message(user_id, message.message_id - 1)

        await bot.send_message(user_id, f"Отправьте фото клада:")
        await bot.delete_message(user_id, message.message_id)
    except:
        pass


async def add_clad_end(message: Message, bot: Bot, state: FSMContext):
    try:
        user_id = message.chat.id
        context_data = await state.get_data()
        city_add = context_data.get('city_clad')
        city = str(city_add)
        area_add = context_data.get('area_clad')
        area = str(area_add)
        tovar_add = context_data.get('tovar_clad')
        tovar = str(tovar_add)
        gram_add = context_data.get('gram_clad')
        gram = str(gram_add)
        price_add = context_data.get('price_clad')
        price = str(price_add)
        latitude_add = context_data.get('latit')
        latitude = str(latitude_add)
        longtitude_add = context_data.get('longtit')
        longtitude = str(longtitude_add)
        if message.photo:
            photo_url = message.photo[-1].file_id
        else:
            photo_url = None
        await bot.delete_message(message.chat.id, message.message_id - 1)
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clad (name_city, name_area, name_item, name_gram, price_item, latitude, longtitude, photo_clad) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (city, area, tovar, gram, price, latitude, longtitude, photo_url))

        # Применение изменений и закрытие соединения с базой данных
        conn.commit()
        conn.close()
        key_item = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
            ]
        ])
        await bot.send_photo(message.chat.id, photo_url, caption=f" Город: {city}\n"
                                                                 f"Район:{area}\n"
                                                                 f"Товар:{tovar}\n"
                                                                 f"Граммовка:{gram}\n"
                                                                 f"Цена:{price}\n"
                                                                 f"Долгота:{latitude}\n"
                                                                 f"Широта:{longtitude}\n"
                                                                 f"Клад успешно добавлен! ✅", reply_markup=key_item)
        await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def del_clad(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id
        await state.set_state(Clad.del_clad)

        await bot.send_message(user_id, f"Введите ID клада который хотите удалить:")
        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass

async def del_clad_end(message: Message, bot: Bot):
    try:
        id_clad = message.text
        user_id = message.chat.id
        await bot.delete_message(user_id, message.message_id - 1)
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clad WHERE id=?", (id_clad,))
        conn.commit()
        conn.close()
        key_item = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
            ]
        ])
        await bot.send_message(user_id, f"Клад по ID:({id_clad}) успешно удалён! ✅", reply_markup=key_item)
        await bot.delete_message(user_id, message.message_id)
    except:
        pass

async def show_clad(call: CallbackQuery, bot: Bot):
    try:
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT name_city FROM clad')
        rows = cursor.fetchall()
        conn.close()
        key_city = InlineKeyboardMarkup(inline_keyboard=[])

        if len(rows) > 0:
            for i in range(0, len(rows), 2):
                row = []
                # Добавляем две кнопки в строку, если есть два города
                if i < len(rows) - 1:
                    row.append(InlineKeyboardButton(text=rows[i][0], callback_data=f'city_admin_show_{rows[i][0]}'))
                    row.append(
                        InlineKeyboardButton(text=rows[i + 1][0], callback_data=f'city_admin_show_{rows[i + 1][0]}'))
                else:
                    row.append(InlineKeyboardButton(text=rows[i][0], callback_data=f'city_admin_show_{rows[i][0]}'))
                key_city.inline_keyboard.append(row)
            key_city.inline_keyboard.append([
                InlineKeyboardButton(text="Назад 🔙", callback_data=f'admin_clad')
            ])
            await bot.send_message(call.message.chat.id, "Выберите город:", reply_markup=key_city)
            await bot.delete_message(call.message.chat.id, call.message.message_id)

        else:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])
            await bot.send_message(call.message.chat.id, "Нет доступных городов. \n",reply_markup=key_item)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

async def show_clad_item(call: CallbackQuery, bot: Bot):
    try:
        city = call.data.split('_')[3]
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name_item FROM clad WHERE name_city = ?", (city,))
        rows = cursor.fetchall()
        conn.close()
        key_city = InlineKeyboardMarkup(inline_keyboard=[])

        if len(rows) > 0:
            for i in range(0, len(rows), 2):
                row = []
                # Добавляем две кнопки в строку, если есть два города
                if i < len(rows) - 1:
                    row.append(InlineKeyboardButton(text=rows[i][0], callback_data=f'admin_show_item_{rows[i][0]}_{city}'))
                    row.append(
                        InlineKeyboardButton(text=rows[i + 1][0], callback_data=f'admin_show_item_{rows[i + 1][0]}_{city}'))
                else:
                    row.append(InlineKeyboardButton(text=rows[i][0], callback_data=f'admin_show_item_{rows[i][0]}_{city}'))
                key_city.inline_keyboard.append(row)
            key_city.inline_keyboard.append([
                InlineKeyboardButton(text="Назад 🔙", callback_data=f'show_clad_set_')
            ])
            await bot.send_message(call.message.chat.id, f"Город {city}\n"
                                                         "Выберите Товар :", reply_markup=key_city)
            await bot.delete_message(call.message.chat.id, call.message.message_id)

        else:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])
            await bot.send_message(call.message.chat.id, "Нет доступных товаров. \n", reply_markup=key_item)
            await bot.delete_message(call.message.chat.id, call.message.message_id)

    except Exception as e:
        print(repr(e))


async def show_clad_area(call: CallbackQuery, bot: Bot):
    try:
        item = call.data.split('_')[3]
        city = call.data.split('_')[4]
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name_area FROM clad WHERE name_city = ? AND name_item = ?", (city, item))
        rows = cursor.fetchall()
        conn.close()
        key_city = InlineKeyboardMarkup(inline_keyboard=[])

        if len(rows) > 0:
            for i in range(0, len(rows), 2):
                row = []
                # Добавляем две кнопки в строку, если есть два города
                if i < len(rows) - 1:
                    row.append(InlineKeyboardButton(text=rows[i][0], callback_data=f'gram_admin_show_{rows[i][0]}_{item}_{city}'))
                    row.append(
                        InlineKeyboardButton(text=rows[i + 1][0], callback_data=f'gram_admin_show_{rows[i][0]}_{item}_{city}'))
                else:
                    row.append(InlineKeyboardButton(text=rows[i][0], callback_data=f'gram_admin_show_{rows[i][0]}_{item}_{city}'))
                key_city.inline_keyboard.append(row)
            key_city.inline_keyboard.append([
                InlineKeyboardButton(text="Назад 🔙", callback_data=f'city_admin_show_{city}')
            ])
            await bot.send_message(call.message.chat.id, f"Город {city}\nТовар {item}\n"
                                                         "Выберите Район:", reply_markup=key_city)
            await bot.delete_message(call.message.chat.id, call.message.message_id)

        else:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])
            await bot.send_message(call.message.chat.id, "Нет доступных районов. \n", reply_markup=key_item)
            await bot.delete_message(call.message.chat.id, call.message.message_id)

    except:
        pass

async def show_clad_gram(call: CallbackQuery, bot: Bot):
    try:
        area = call.data.split('_')[3]
        item = call.data.split('_')[4]
        city = call.data.split('_')[5]
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name_gram, COUNT(*) FROM clad WHERE name_city = ? AND name_item = ? AND name_area = ? GROUP BY name_gram", (city, item, area))
        rows = cursor.fetchall()
        conn.close()
        key_city = InlineKeyboardMarkup(inline_keyboard=[])

        if len(rows) > 0:
            for row in rows:
                gram, count = row
                key_city.inline_keyboard.append([
                    InlineKeyboardButton(text=f'{gram} грамм - {count} кладов', callback_data=f'end_clad_show_{gram}_{city}_{item}_{area}')
                ])
            key_city.inline_keyboard.append([
                InlineKeyboardButton(text="Назад 🔙", callback_data=f'admin_show_item_{item}_{city}')
            ])
            await bot.send_message(call.message.chat.id, f"Город {city}\nТовар {item}\n"
                                                         f"Район {area}\nВыберите Граммовку:", reply_markup=key_city)
            await bot.delete_message(call.message.chat.id, call.message.message_id)

        else:
            key_item = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
                ]
            ])
            await bot.send_message(call.message.chat.id, "Нет доступных граммовок.\n", reply_markup=key_item)
            await bot.delete_message(call.message.chat.id, call.message.message_id)

    except Exception as e:
        print(f"An error occurred: {e}")

async def show_clad_end(call: CallbackQuery, bot: Bot):
    try:
        gram = call.data.split('_')[3]
        city = call.data.split('_')[4]
        item = call.data.split('_')[5]
        area = call.data.split('_')[6]

        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, name_city, name_area, name_item, name_gram, price_item, latitude, longtitude, photo_clad FROM clad WHERE name_city = ? AND name_area = ? AND name_item = ? AND name_gram = ?', (city, area, item, gram))
        clads = cursor.fetchall()
        conn.close()
        key_item = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')
            ]
        ])
        if clads:
            photo_new = None
            message_text = "Список кладов:\n"
            for clad in clads:
                clad_id, name_city, name_area, name_item, name_gram, price_item, latitude, longtitude, photo = clad
                message_text += f"ID: {clad_id}\n"
                message_text += f"Город: {name_city}\n"
                message_text += f"Район: {name_area}\n"
                message_text += f"Товар: {name_item}\n"
                message_text += f"Граммовка: {name_gram}\n"
                message_text += f"Цена: {price_item}\n"
                message_text += f"Широта: {latitude}\n"
                message_text += f"Долгота: {longtitude}\n\n"
                photo_new = photo
            await bot.send_photo(call.message.chat.id, photo=photo_new, caption=message_text, reply_markup=key_item)
            await bot.delete_message(call.message.chat.id, call.message.message_id)

        else:
            await bot.send_message(call.message.chat.id, "Нет зарегистрированных кладов.", reply_markup=key_item)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass