from aiogram import Bot
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
import sqlite3
import re
from utils.state import Rass, City, Admin, Area, Item, Gram, Balance, Balance_del, Clad
import logging
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

async def admin_analis(call: CallbackQuery, bot: Bot):
    try:
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name_city FROM city")
        cities = cursor.fetchall()
        conn.close()

        if cities:
            key_city = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text=city[0], callback_data=f'_analis_city_{city[0]}') for city in cities
                ],
                [
                    InlineKeyboardButton(text="Назад", callback_data='admin_command')
                ]
            ])
            await bot.send_message(call.message.chat.id, "Выберите город для просмотра статистики", reply_markup=key_city)

        else:
            key_city = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Назад", callback_data='admin_command')
                ]
            ])
            await bot.send_message(call.message.chat.id, "У вас нет городов для просмотра статистики.",
                                   reply_markup=key_city)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

async def admin_analis_mid(call: CallbackQuery, bot: Bot):
    try:
        city = call.data.split('_')[3]
        key_city = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Месяц", callback_data=f'_analis_mont_{city}')
            ],
            [
                InlineKeyboardButton(text="Неделя", callback_data=f'_analis_week_{city}')
            ],
            [
                InlineKeyboardButton(text="День", callback_data=f'_analis_day_{city}')
            ],
            [
                InlineKeyboardButton(text="Назад", callback_data='admin_command')
            ]
        ])
        await bot.send_message(call.message.chat.id, "Выберите период для просмотра статистики.",
                               reply_markup=key_city)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

async def admin_analis_mont_st(call: CallbackQuery, bot: Bot):
    try:
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT mont FROM analist")
        monts = cursor.fetchall()
        conn.close()
        city = call.data.split('_')[3]

        key_city = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=mont[0], callback_data=f"analis_monest_{mont[0]}_{city}") for mont in monts],
            [InlineKeyboardButton(text="Назад", callback_data='admin_command')]
        ])
        await bot.send_message(call.message.chat.id, text=f"Город {city}\nВыберите месяц для анализа :",
                               reply_markup=key_city)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
async def admin_analis_mont(call: CallbackQuery, bot: Bot):
    try:
        mont = call.data.split('_')[2]
        city = call.data.split('_')[3]
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        query = '''
            SELECT
                item,
                SUM(CAST(col AS INTEGER)) AS total_col,
                SUM(CAST(price AS INTEGER)) AS total_price
            FROM
                analist
            WHERE
                mont = ? AND city = ?
            GROUP BY
                item
        '''
        cursor.execute(query, (str(mont), city))

        results = cursor.fetchall()

        message_text = f"Статистика по текущему месяцу для города {city}:\n"
        for row in results:
            item, total_col, total_price = row
            message_text += f'Товар: {item}\nОбщее количество: {total_col}\nОбщая сумма продажи: {total_price}zl\n\n'

        # Закрываем соединение с базой данных
        conn.close()
        key_city = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Назад", callback_data='admin_command')
            ]
        ])
        await bot.send_message(call.message.chat.id, text=message_text, reply_markup=key_city)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

async def admin_analis_week(call: CallbackQuery, bot: Bot):
    try:
        city = call.data.split('_')[3]
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()

        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Выводим информацию о текущем интервале
        print(
            f"Проверяем дни с {start_of_week.strftime('%Y-%m-%d')} по {end_of_week.strftime('%Y-%m-%d')} для города {city}:")

        query = '''
            SELECT
                item,
                GROUP_CONCAT(DISTINCT day) AS days,
                SUM(CAST(col AS INTEGER)) AS total_col,
                SUM(CAST(price AS INTEGER)) AS total_price
            FROM
                analist
            WHERE
                CAST(day AS INTEGER) = ? AND (mont = ? OR (mont = ? AND CAST(day AS INTEGER) <= ?))
                AND city = ?
            GROUP BY
                item
        '''

        current_date = start_of_week
        message_text = f"Статистика за неделю c {start_of_week.strftime('%Y-%m-%d')} по {end_of_week.strftime('%Y-%m-%d')} для города {city}:\n\n"
        total_price_all_items = 0
        total_col_per_item = {}

        while current_date <= end_of_week:
            print(f"Проверяем день: {current_date.strftime('%Y-%m-%d')}")

            cursor.execute(query, (int(current_date.strftime('%d')), str(current_date.month), str(current_date.month),
                                   int(end_of_week.strftime('%d')), city))
            results = cursor.fetchall()

            if not results:
                message_text += f'Для {current_date.strftime("%Y-%m-%d")} нет продаж в городе {city}\n\n'
            else:
                for row in results:
                    item, days, total_col, total_price = row
                    print(total_price)
                    total_price_all_items += int(total_price)

                    if item in total_col_per_item:
                        total_col_per_item[item] += int(total_col)
                    else:
                        total_col_per_item[item] = int(total_col)

                    message_text += f'Город: {city}\nТовар: {item}\nДаты: {days}\nОбщее количество: {total_col}\nОбщая сумма продажи: {total_price}zl\n\n'

            current_date += timedelta(days=1)
        conn.close()
        print(total_col_per_item)
        message_text += f'Общая сумму продажи всех товар: {total_price_all_items}zl\n'
        print(f"Общая сумма продажи за неделю: {total_price_all_items}")
        for item, total_col in total_col_per_item.items():
            print(f"Общее количество товара {item}: {total_col}")
            message_text += f'Общее количество товара {item}: {total_col}\n'

        key_city = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data='admin_command')]
        ])
        await bot.send_message(call.message.chat.id, text=message_text, reply_markup=key_city)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass


async def admin_analis_day(call: CallbackQuery, bot: Bot):
    try:
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT mont FROM analist")
        monts = cursor.fetchall()
        conn.close()
        city = call.data.split('_')[3]

        key_city = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=mont[0], callback_data=f"analis_montsa_{mont[0]}_{city}")for mont in monts],
            [InlineKeyboardButton(text="Назад", callback_data='admin_command')]
        ])
        await bot.send_message(call.message.chat.id, text=f"Город {city}\nВыберите месяц для анализа :", reply_markup=key_city)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

async def admin_analis_day_mid(call: CallbackQuery, bot: Bot):
    try:
        mont = call.data.split('_')[2]
        city = call.data.split('_')[3]
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()

        # Выбор уникальных дней для текущего месяца
        cursor.execute("SELECT DISTINCT day FROM analist WHERE mont = ?", (mont,))
        days = cursor.fetchall()

        # Закрытие соединения
        conn.close()

        # Создание кнопок для каждого уникального дня в текущем месяце
        key_city = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=day[0], callback_data=f"day_analis_{day[0]}_{mont}_{city}")for day in days
            ],
            [
                InlineKeyboardButton(text="Назад", callback_data='analis_montsa_')
            ]
        ])


        await bot.send_message(call.message.chat.id, text=f"Выберите день для месяца {mont}:", reply_markup=key_city)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

async def admin_analis_day_end(call: CallbackQuery, bot: Bot):
    try:
        day = call.data.split('_')[2]
        mont = call.data.split('_')[3]
        city = call.data.split('_')[4]

        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()

        # Получение текущей даты
        today = datetime.now()

        # Запрос SQL для получения статистики по текущему дню и городу
        query = '''
            SELECT
                item,
                SUM(CAST(col AS INTEGER)) AS total_col,
                SUM(CAST(price AS INTEGER)) AS total_price
            FROM
                analist
            WHERE
                CAST(day AS INTEGER) = ? AND mont = ? AND city = ?
            GROUP BY
                item
        '''

        # Выполнение запроса
        cursor.execute(query, (str(day), str(mont), str(city)))
        results = cursor.fetchall()

        # Закрытие соединения с базой данных
        conn.close()
        message_text = f"Статистика за день-{day} месяца-{mont} в городе {city}:\n\n"

        for row in results:
            item, total_col, total_price = row
            print(f'Tовар: {item}\nОбщее количество: {total_col}\nОбщая сумма продажи: {total_price}zl\n\n')
            message_text += f'Товар: {item}\nОбщее количество: {total_col}\nОбщая сумма продажи: {total_price}zl\n\n'
        key_city = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Выйти в меню", callback_data='admin_command')]
        ])
        await bot.send_message(call.message.chat.id, text=message_text, reply_markup=key_city)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
