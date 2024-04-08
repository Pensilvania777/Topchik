from aiogram import Bot
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
import sqlite3
from datetime import datetime


async def buy_clad(call: CallbackQuery, bot: Bot):
    try:

        launge = call.data.split('_')[2]
        user_id = call.message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM city")
        cities = cursor.fetchall()
        conn.close()
        if len(cities) > 0:
            if launge == "ru":
                conn = sqlite3.connect('shop.db')
                cursor = conn.cursor()
                cursor.execute('''SELECT text_city, photo_city FROM oform_ru WHERE id = ?''', (1,))

                result = cursor.fetchone()
                text_menu = ""
                photo_menu = ""
                if result:
                    text_menu, photo_menu = result
                conn.close()
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text=city[1], callback_data=f'_ars_city_{city[1]}_{launge}')
                        for city in cities
                    ],
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'back_menu_st_{launge}')
                    ]
                ])
                await bot.send_photo(user_id, photo_menu, caption=text_menu, reply_markup=keyboard)

            elif launge == "ua":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text=city[1], callback_data=f'_ars_city_{city[1]}_{launge}')
                        for city in cities
                    ],
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'back_menu_st_{launge}')
                    ]
                ])

                await bot.send_message(call.message.chat.id, "Виберіть місто:", reply_markup=keyboard)
            elif launge == "en":
                conn = sqlite3.connect('shop.db')
                cursor = conn.cursor()
                cursor.execute('''SELECT text_city, photo_city FROM oform_en WHERE id = ?''', (1,))

                result = cursor.fetchone()
                text_menu = ""
                photo_menu = ""
                if result:
                    text_menu, photo_menu = result
                conn.close()
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text=city[1], callback_data=f'_ars_city_{city[1]}_{launge}')
                        for city in cities
                    ],
                    [
                        InlineKeyboardButton(text="Back 🔙", callback_data=f'back_menu_st_{launge}')
                    ]
                ])
                await bot.send_photo(user_id, photo_menu, caption=text_menu, reply_markup=keyboard)
            elif launge == "pl":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text=city[1], callback_data=f'_ars_city_{city[1]}_{launge}')
                        for city in cities
                    ],
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'back_menu_st_{launge}')
                    ]
                ])
                await bot.send_message(call.message.chat.id, "Wybierz miasto:", reply_markup=keyboard)

            # Отправляем сообщение с инлайновыми кнопками
            await bot.delete_message(call.message.chat.id, call.message.message_id)

        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Назад 🔙", callback_data='back_menu_st_')
                ]
            ])
            await bot.send_message(call.message.chat.id, f"Нет Города.", reply_markup=keyboard)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(repr(e))

async def buy_item(call: CallbackQuery, bot: Bot):
    try:

        city = call.data.split('_')[3]
        launge = call.data.split('_')[4]

        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT name_item FROM clad WHERE name_city = ?", (city,))
        unique_items = cursor.fetchall()
        conn.close()

        if len(unique_items) > 0:
            if launge == "ru":
                conn = sqlite3.connect('shop.db')
                cursor = conn.cursor()
                cursor.execute('''SELECT text_item, photo_item FROM oform_ru WHERE id = ?''', (1,))

                result = cursor.fetchone()
                text_menu = ""
                photo_menu = ""
                if result:
                    text_menu, photo_menu = result
                conn.close()
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                                                                    [
                                                                        InlineKeyboardButton(text=item[0],
                                                                                             callback_data=f'_ars_item_{city}_{item[0]}_{launge}')
                                                                    ]
                                                                    for item in unique_items
                                                                ] + [
                                                                    [InlineKeyboardButton(text="Назад 🔙",
                                                                                          callback_data=f'buy_clad_{launge}')]
                                                                ])

                await bot.send_photo(call.message.chat.id, photo_menu, caption=text_menu, reply_markup=keyboard)


            elif launge == "ua":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                                                                    [
                                                                        InlineKeyboardButton(text=item[0],
                                                                                             callback_data=f'_ars_item_{city}_{item[0]}_{launge}')
                                                                    ]
                                                                    for item in unique_items
                                                                ] + [
                                                                    [InlineKeyboardButton(text="Назад 🔙",
                                                                                          callback_data=f'buy_clad_{launge}')]
                                                                ])

                await bot.send_message(call.message.chat.id, f"Місто({city})\n"
                                                             f"Виберіть товар:", reply_markup=keyboard)

            elif launge == "en":
                conn = sqlite3.connect('shop.db')
                cursor = conn.cursor()
                cursor.execute('''SELECT text_item, photo_item FROM oform_en WHERE id = ?''', (1,))

                result = cursor.fetchone()
                text_menu = ""
                photo_menu = ""
                if result:
                    text_menu, photo_menu = result
                conn.close()
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                                                                    [
                                                                        InlineKeyboardButton(text=item[0],
                                                                                             callback_data=f'_ars_item_{city}_{item[0]}_{launge}')
                                                                    ]
                                                                    for item in unique_items
                                                                ] + [
                                                                    [InlineKeyboardButton(text="Back 🔙",
                                                                                          callback_data=f'buy_clad_{launge}')]
                                                                ])

                await bot.send_photo(call.message.chat.id, photo_menu, caption=text_menu, reply_markup=keyboard)


            elif launge == "pl":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                                                                    [
                                                                        InlineKeyboardButton(text=item[0],
                                                                                             callback_data=f'_ars_item_{city}_{item[0]}_{launge}')
                                                                    ]
                                                                    for item in unique_items
                                                                ] + [
                                                                    [InlineKeyboardButton(text="Z powrotem 🔙",
                                                                                          callback_data=f'buy_clad_{launge}')]
                                                                ])

                await bot.send_message(call.message.chat.id, f"Miasto({city})\n"
                                                             f"Wybierz produkt:", reply_markup=keyboard)

            await bot.delete_message(call.message.chat.id, call.message.message_id)

        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Назад 🔙", callback_data=f'buy_clad_{launge}')
                ],
                [
                    InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')
                ]
            ])
            await bot.send_message(call.message.chat.id, f"Город({city})\n"
                                                         f"Товар не найден.", reply_markup=keyboard)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(repr(e))


async def buy_area(call: CallbackQuery, bot: Bot):
    try:
        city = call.data.split('_')[3]
        launge = call.data.split('_')[5]
        item = call.data.split('_')[4]
        print(city,item, launge)
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name_area FROM clad WHERE name_city = ? AND name_item = ?", (city, item))
        areas = cursor.fetchall()
        conn.close()
        if len(areas) > 0:
            if launge == "ru":
                conn = sqlite3.connect('shop.db')
                cursor = conn.cursor()
                cursor.execute('''SELECT text_area, photo_area FROM oform_ru WHERE id = ?''', (1,))

                result = cursor.fetchone()
                text_menu = ""
                photo_menu = ""
                if result:
                    text_menu, photo_menu = result
                conn.close()
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text=area[0], callback_data=f'_ars_area_{city}_{area[0]}_{launge}_{item}')
                        for area in areas
                    ],
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_city_{city}_{launge}')
                    ]
                ])
                await bot.send_photo(call.message.chat.id, photo_menu, caption=text_menu, reply_markup=keyboard)

            elif launge == "ua":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text=area[0], callback_data=f'_ars_area_{city}_{area[0]}_{launge}_{item}')
                        for area in areas
                    ],
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_city_{city}_{launge}')
                    ]
                ])
                await bot.send_message(call.message.chat.id, f"Виберіть район у місті {city}:", reply_markup=keyboard)

            elif launge == "en":
                conn = sqlite3.connect('shop.db')
                cursor = conn.cursor()
                cursor.execute('''SELECT text_area, photo_area FROM oform_en WHERE id = ?''', (1,))

                result = cursor.fetchone()
                text_menu = ""
                photo_menu = ""
                if result:
                    text_menu, photo_menu = result
                conn.close()
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text=area[0], callback_data=f'_ars_area_{city}_{area[0]}_{launge}_{item}')
                        for area in areas
                    ],
                    [
                        InlineKeyboardButton(text="Back 🔙", callback_data=f'_ars_city_{city}_{launge}')
                    ]
                ])
                await bot.send_photo(call.message.chat.id, photo_menu, caption=text_menu, reply_markup=keyboard)

            elif launge == "pl":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text=area[0], callback_data=f'_ars_area_{city}_{area[0]}_{launge}_{item}')
                        for area in areas
                    ],
                    [
                        InlineKeyboardButton(text="Z powrotem 🔙", callback_data=f'_ars_city_{city}_{launge}')
                    ]
                ])
                await bot.send_message(call.message.chat.id, f"Wybierz obszar w mieście {city}:", reply_markup=keyboard)
            await bot.delete_message(call.message.chat.id, call.message.message_id)

        else:
            if launge == "ru":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_city_{city}_{launge}'),
                        InlineKeyboardButton(text="Меню 💫", callback_data=f'back_menu_st_{launge}')
                    ],

                ])
                await bot.send_message(call.message.chat.id, f" В городе {city} нет районов.", reply_markup=keyboard)

            elif launge == "ua":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_city_{city}_{launge}'),
                        InlineKeyboardButton(text="Меню 💫", callback_data=f'back_menu_st_{launge}')
                    ],

                ])
                await bot.send_message(call.message.chat.id, f" У місті {city} немає районів.", reply_markup=keyboard)
            elif launge == "en":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_city_{city}_{launge}'),
                        InlineKeyboardButton(text="Меню 💫", callback_data=f'back_menu_st_{launge}')
                    ],

                ])
                await bot.send_message(call.message.chat.id, f"There are no districts in {city}.", reply_markup=keyboard)

            elif launge == "pl":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Z powrotem 🔙", callback_data=f'_ars_city_{city}_{launge}'),
                        InlineKeyboardButton(text="Menu 💫", callback_data=f'back_menu_st_{launge}')
                    ],

                ])
                await bot.send_message(call.message.chat.id, f"Brak dzielnic w {city}.", reply_markup=keyboard)

            await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(repr(e))


async def buy_gram(call: CallbackQuery, bot: Bot):
    try:
        city = call.data.split('_')[3]
        area = call.data.split('_')[4]
        item = call.data.split('_')[6]
        launge = call.data.split('_')[5]
        print(city, area, item ,launge)

        itemsnow = item

        print(city, area, item)
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM item WHERE name_item = ?", (item,))
        items = cursor.fetchall()
        conn.close()
        if len(items) > 0:
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute("SELECT name_gram FROM clad WHERE name_city = ? AND name_area = ? AND name_item = ?",
                           (city, area, itemsnow))
            grams = cursor.fetchall()
            conn.close()
            name_item = ""
            caption_item = ""
            price_item = ""
            for item in items:
                name_item = item[1]
                caption_item = item[2]
                price_item = item[3]
            photo_data = item[4]
            unique_grams = ""
            for gram in grams:
                unique_grams = gram[0]
            print(unique_grams)

            if launge == "ru":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text=unique_grams,
                                             callback_data=f'_ars_gram_{city}_{area}_{itemsnow}_{unique_grams}_{launge}')
                    ],
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_item_{city}_{itemsnow}_{launge}')
                    ]
                ])
                await bot.send_photo(call.message.chat.id, photo_data, caption=f"Товар: {name_item}\n"
                                                                               f"Описание: {caption_item}\n"
                                                                               f"Цена за грамм : {price_item}\n"
                                                                               f"Выберите граммовку:",
                                     reply_markup=keyboard)

            elif launge == "ua":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text=grame[0],
                                             callback_data=f'_ars_gram_{city}_{area}_{itemsnow}_{grame[0]}_{launge}')
                        for grame in grams

                    ],
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_item_{city}_{itemsnow}_{launge}')
                    ]
                ])
                await bot.send_photo(call.message.chat.id, photo_data, caption=f"Товар: {name_item}\n"
                                                                               f"Опис: {caption_item}\n"
                                                                               f"Ціна за грам: {price_item}\n"
                                                                               f"Виберіть грамування:",
                                     reply_markup=keyboard)
            elif launge == "en":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text=grame[0],
                                             callback_data=f'_ars_gram_{city}_{area}_{itemsnow}_{grame[0]}_{launge}')
                        for grame in grams

                    ],
                    [
                        InlineKeyboardButton(text="Back 🔙", callback_data=f'_ars_item_{city}_{itemsnow}_{launge}')
                    ]
                ])
                await bot.send_photo(call.message.chat.id, photo_data, caption=f"Product: {name_item}\n"
                                                                               f"Description: {caption_item}\n"
                                                                               f"Price per gram: {price_item}\n"
                                                                               f"Select grammar:",
                                     reply_markup=keyboard)

            elif launge == "pl":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text=grame[0],
                                             callback_data=f'_ars_gram_{city}_{area}_{itemsnow}_{grame[0]}_{launge}')
                        for grame in grams

                    ],
                    [
                        InlineKeyboardButton(text="Z powrotem 🔙", callback_data=f'_ars_item_{city}_{itemsnow}_{launge}')
                    ]
                ])
                await bot.send_photo(call.message.chat.id, photo_data, caption=f"Produkt: {name_item}\n"
                                                                               f"Opis: {caption_item}\n"
                                                                               f"Cena za gram: {price_item}\n"
                                                                               f"Wybierz gramatykę:",
                                     reply_markup=keyboard)

            await bot.delete_message(call.message.chat.id, call.message.message_id)
        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_item_{city}_{itemsnow}_{launge}')
                ],
                [
                    InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')
                ]

            ])

            await bot.send_message(call.message.chat.id, f"Город({city})\n"
                                                         f"Район({area})\n"
                                                         f"Товар не найден.", reply_markup=keyboard)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(e)


async def buy_item_end(call: CallbackQuery, bot: Bot):
    try:
        user_id = call.message.chat.id
        city = call.data.split('_')[3]
        area = call.data.split('_')[4]
        item = call.data.split('_')[5]
        gram = call.data.split('_')[6]
        launge = call.data.split('_')[7]
        print(city,area,item,gram,launge)
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT price_item, latitude, longtitude FROM clad WHERE name_city = ? AND name_area = ? AND name_item = ? AND name_gram = ?",
            (city, area, item, gram))

        result = cursor.fetchone()
        conn.close()
        if result:
            price_item, latitude, longtitude = result
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM item WHERE name_item = ?", (item,))
            rare = cursor.fetchone()
            conn.close()

            if rare:

                name_item = rare[1]
                caption_item = rare[2]
                price = rare[3]
                photo_data = rare[4]

                conn = sqlite3.connect('shop.db')
                cursor = conn.cursor()
                cursor.execute("SELECT col_sale FROM refferrs WHERE user_id = ?", (user_id,))
                result = cursor.fetchone()
                conn.close()
                print(price_item)
                discount_amount = 0.10 * int(price_item)
                if result is None:
                    if launge == "ru":
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Купить ✅",
                                                     callback_data=f'_ars_end_{city}_{area}_{item}_{gram}_{price_item}_{latitude}_{longtitude}_{launge}')
                            ] +
                            [
                                InlineKeyboardButton(text="Отменить ❌", callback_data=f'back_menu_st_{city}_{area}_{item}')
                            ],
                            [
                                InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_data, caption=f"Товар: {name_item}\n"
                                                                                       f"Описание: {caption_item}\n"
                                                                                       f"Цена за грамм: {price} zl\n"
                                                                                       f"Граммовка: {gram} грамм\n"
                                                                                       f"Цена: {price_item} zl\n",
                                             reply_markup=keyboard)

                    elif launge == "ua":
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Придбати ✅",
                                                     callback_data=f'_ars_end_{city}_{area}_{item}_{gram}_{price_item}_{latitude}_{longtitude}_{launge}')
                            ] +
                            [
                                InlineKeyboardButton(text="Скасувати ❌", callback_data=f'back_menu_st_{city}_{area}_{item}')
                            ],
                            [
                                InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_data, caption=f"Товар: {name_item}\n"
                                                                                       f"Опис: {caption_item}\n"
                                                                                       f"Ціна за грам: {price} zl\n"
                                                                                       f"Грамування: {gram} грам\n"
                                                                                       f"Ціна: {price_item} zl\n",
                                             reply_markup=keyboard)
                    elif launge == "en":
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Buy ✅",
                                                     callback_data=f'_ars_end_{city}_{area}_{item}_{gram}_{price_item}_{latitude}_{longtitude}_{launge}')
                            ] +
                            [
                                InlineKeyboardButton(text="Cancel ❌", callback_data=f'back_menu_st_{city}_{area}_{item}')
                            ],
                            [
                                InlineKeyboardButton(text="Back 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_data, caption=f"Product: {name_item}\n"
                                                                                       f"Description: {caption_item}\n"
                                                                                       f"Price per gram: {price} zl\n"
                                                                                       f"Gram: {gram} gram\n"
                                                                                       f"Price: {price_item} zl\n",
                                             reply_markup=keyboard)
                    elif launge == "pl":
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Kupić ✅",
                                                     callback_data=f'_ars_end_{city}_{area}_{item}_{gram}_{price_item}_{latitude}_{longtitude}_{launge}')
                            ] +
                            [
                                InlineKeyboardButton(text="Anulować ❌", callback_data=f'back_menu_st_{city}_{area}_{item}')
                            ],
                            [
                                InlineKeyboardButton(text="Z powrotem 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_data, caption=f"Produkt: {name_item}\n"
                                                                                       f"Opis: {caption_item}\n"
                                                                                       f"Cena za gram: {price} zł\n"
                                                                                       f"Gram: {gram} gram\n"
                                                                                       f"Cena: {price_item} zł\n",
                                             reply_markup=keyboard)

                    await bot.delete_message(call.message.chat.id, call.message.message_id)

                elif result[0] > 0:
                    print(discount_amount)
                    price_item_sale = price_item - discount_amount
                    if launge == "ru":
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Купить ✅",
                                                     callback_data=f'_ars_end_{city}_{area}_{item}_{gram}_{price_item_sale}_{latitude}_{longtitude}_{launge}')
                            ] +
                            [
                                InlineKeyboardButton(text="Отменить ❌", callback_data=f'back_menu_st_{city}_{area}_{item}')
                            ],
                            [
                                InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_data, caption=f"Товар: {name_item}\n"
                                                                                       f"Описание: {caption_item}\n"
                                                                                       f"Цена за грамм: {price} zl\n"
                                                                                       f"Граммовка: {gram} грамм\n"
                                                                                       f"Цена: {price_item} zl\n",
                                             reply_markup=keyboard)

                    elif launge == "ua":
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Придбати ✅",
                                                     callback_data=f'_ars_end_{city}_{area}_{item}_{gram}_{price_item_sale}_{latitude}_{longtitude}_{launge}')
                            ] +
                            [
                                InlineKeyboardButton(text="Скасувати ❌", callback_data=f'back_menu_st_{city}_{area}_{item}')
                            ],
                            [
                                InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_data, caption=f"Товар: {name_item}\n"
                                                                                       f"Опис: {caption_item}\n"
                                                                                       f"Ціна за грам: {price} zl\n"
                                                                                       f"Грамування: {gram} грам\n"
                                                                                       f"Ціна: {price_item} zl\n",
                                             reply_markup=keyboard)
                    elif launge == "en":
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Buy ✅",
                                                     callback_data=f'_ars_end_{city}_{area}_{item}_{gram}_{price_item_sale}_{latitude}_{longtitude}_{launge}')
                            ] +
                            [
                                InlineKeyboardButton(text="Cancel ❌", callback_data=f'back_menu_st_{city}_{area}_{item}')
                            ],
                            [
                                InlineKeyboardButton(text="Back 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_data, caption=f"Product: {name_item}\n"
                                                                                       f"Description: {caption_item}\n"
                                                                                       f"Price per gram: {price} zl\n"
                                                                                       f"Gram: {gram} gram\n"
                                                                                       f"Price: {price_item} zl\n",
                                             reply_markup=keyboard)
                    elif launge == "pl":
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Kupić ✅",
                                                     callback_data=f'_ars_end_{city}_{area}_{item}_{gram}_{price_item_sale}_{latitude}_{longtitude}_{launge}')
                            ] +
                            [
                                InlineKeyboardButton(text="Anulować ❌", callback_data=f'back_menu_st_{city}_{area}_{item}')
                            ],
                            [
                                InlineKeyboardButton(text="Z powrotem 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_data, caption=f"Produkt: {name_item}\n"
                                                                                       f"Opis: {caption_item}\n"
                                                                                       f"Cena za gram: {price} zł\n"
                                                                                       f"Gram: {gram} gram\n"
                                                                                       f"Cena: {price_item} zł\n",
                                             reply_markup=keyboard)

                    await bot.delete_message(call.message.chat.id, call.message.message_id)

                else:
                    if launge == "ru":
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Купить ✅",
                                                     callback_data=f'_ars_end_{city}_{area}_{item}_{gram}_{price_item}_{latitude}_{longtitude}_{launge}')
                            ] +
                            [
                                InlineKeyboardButton(text="Отменить ❌", callback_data=f'back_menu_st_{city}_{area}_{item}')
                            ],
                            [
                                InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_data, caption=f"Товар: {name_item}\n"
                                                                                       f"Описание: {caption_item}\n"
                                                                                       f"Цена за грамм: {price} zl\n"
                                                                                       f"Граммовка: {gram} грамм\n"
                                                                                       f"Цена: {price_item} zl\n",
                                             reply_markup=keyboard)

                    elif launge == "ua":
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Придбати ✅",
                                                     callback_data=f'_ars_end_{city}_{area}_{item}_{gram}_{price_item}_{latitude}_{longtitude}_{launge}')
                            ] +
                            [
                                InlineKeyboardButton(text="Скасувати ❌", callback_data=f'back_menu_st_{city}_{area}_{item}')
                            ],
                            [
                                InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_data, caption=f"Товар: {name_item}\n"
                                                                                       f"Опис: {caption_item}\n"
                                                                                       f"Ціна за грам: {price} zl\n"
                                                                                       f"Грамування: {gram} грам\n"
                                                                                       f"Ціна: {price_item} zl\n",
                                             reply_markup=keyboard)
                    elif launge == "en":
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Buy ✅",
                                                     callback_data=f'_ars_end_{city}_{area}_{item}_{gram}_{price_item}_{latitude}_{longtitude}_{launge}')
                            ] +
                            [
                                InlineKeyboardButton(text="Cancel ❌", callback_data=f'back_menu_st_{city}_{area}_{item}')
                            ],
                            [
                                InlineKeyboardButton(text="Back 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_data, caption=f"Product: {name_item}\n"
                                                                                       f"Description: {caption_item}\n"
                                                                                       f"Price per gram: {price} zl\n"
                                                                                       f"Gram: {gram} gram\n"
                                                                                       f"Price: {price_item} zl\n",
                                             reply_markup=keyboard)
                    elif launge == "pl":
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Kupić ✅",
                                                     callback_data=f'_ars_end_{city}_{area}_{item}_{gram}_{price_item}_{latitude}_{longtitude}_{launge}')
                            ] +
                            [
                                InlineKeyboardButton(text="Anulować ❌", callback_data=f'back_menu_st_{city}_{area}_{item}')
                            ],
                            [
                                InlineKeyboardButton(text="Z powrotem 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_data, caption=f"Produkt: {name_item}\n"
                                                                                       f"Opis: {caption_item}\n"
                                                                                       f"Cena za gram: {price} zł\n"
                                                                                       f"Gram: {gram} gram\n"
                                                                                       f"Cena: {price_item} zł\n",
                                             reply_markup=keyboard)

                    await bot.delete_message(call.message.chat.id, call.message.message_id)


            else:
                if launge == "ru":
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [
                            InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')
                        ],
                        [
                            InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                        ]
                    ])

                    await bot.send_message(call.message.chat.id, f"Город({city})\n"
                                                                 f"Район({area})\n"
                                                                 f"Товар не найден.", reply_markup=keyboard)

                elif launge == "ua":
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [
                            InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')
                        ],
                        [
                            InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                        ]
                    ])

                    await bot.send_message(call.message.chat.id, f"Місто({city})\n"
                                                                 f"Район({area})\n"
                                                                 f"Товар не знайдено.", reply_markup=keyboard)

                elif launge == "en":
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [
                            InlineKeyboardButton(text="Menu 💫", callback_data='back_menu_st_')
                        ],
                        [
                            InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                        ]
                    ])

                    await bot.send_message(call.message.chat.id, f"City({city})\n"
                                                                 f"Area({area})\n"
                                                                 f"Product not found.", reply_markup=keyboard)

                elif launge == "pl":

                    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [
                            InlineKeyboardButton(text="Menu 💫", callback_data='back_menu_st_')
                        ],
                        [
                            InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                        ]
                    ])

                    await bot.send_message(call.message.chat.id, f"Miasto({city})\n"
                                                                 f"Obszar({area})\n"
                                                                 f"Nie znaleziono produktu.", reply_markup=keyboard)

                await bot.delete_message(call.message.chat.id, call.message.message_id)
        else:
            if launge == "ru":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')
                    ],
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                    ]
                ])

                await bot.send_message(call.message.chat.id, f"Город({city})\n"
                                                             f"Район({area})\n"
                                                             f"Товар не найден.", reply_markup=keyboard)

            elif launge == "ua":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')
                    ],
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                    ]
                ])

                await bot.send_message(call.message.chat.id, f"Місто({city})\n"
                                                             f"Район({area})\n"
                                                             f"Товар не знайдено.", reply_markup=keyboard)

            elif launge == "en":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Menu 💫", callback_data='back_menu_st_')
                    ],
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                    ]
                ])

                await bot.send_message(call.message.chat.id, f"City({city})\n"
                                                             f"Area({area})\n"
                                                             f"Product not found.", reply_markup=keyboard)

            elif launge == "pl":

                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Menu 💫", callback_data='back_menu_st_')
                    ],
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                    ]
                ])

                await bot.send_message(call.message.chat.id, f"Miasto({city})\n"
                                                             f"Obszar({area})\n"
                                                             f"Nie znaleziono produktu.", reply_markup=keyboard)
    except Exception as e:
        print(repr(e))


async def buy_end_ars(call: CallbackQuery, bot: Bot):
    try:
        city = call.data.split('_')[3]
        area = call.data.split('_')[4]
        item = call.data.split('_')[5]
        gram = call.data.split('_')[6]
        price_item_summ = call.data.split('_')[7]
        long = call.data.split('_')[8]
        lat = call.data.split('_')[9]
        launge = call.data.split('_')[10]

        external_id = call.message.chat.id

        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users_shop WHERE external_id = ?", (external_id,))
        balance = cursor.fetchone()
        conn.close()
        keyboard_cancel = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')
            ]
        ])
        if balance is not None:
            balance_value = balance[0]
            print(balance_value)
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, price_item, latitude, longtitude, photo_clad FROM clad WHERE name_city = ? AND name_area = ? AND name_item = ? AND name_gram = ?",
                (city, area, item, gram))

            result = cursor.fetchone()
            conn.close()
            if result:
                id_item, price_item, latitude, longtitude, photo_clad = result
                balance_final = int(balance_value)
                price_final = int(price_item_summ)
                if balance_final >= price_final:
                    summ_balance = balance_final - int(price_item_summ)
                    conn = sqlite3.connect('shop.db')
                    cursor = conn.cursor()
                    cursor.execute("UPDATE users_shop SET balance = ? WHERE external_id = ?", (summ_balance, external_id))
                    conn.commit()
                    conn.close()
                    conn = sqlite3.connect('shop.db')
                    cursor = conn.cursor()
                    cursor.execute('''INSERT INTO active_clad ( external_id ,name_city, name_area, name_item, name_gram, price_item, latitude, longtitude, photo_clad)
                                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                        external_id, city, area, item, gram, price_item, latitude, longtitude, photo_clad))
                    conn.commit()
                    conn.close()

                    conn = sqlite3.connect('shop.db')
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM clad WHERE id = ?", (id_item,))
                    conn.commit()
                    conn.close()

                    print(summ_balance)

                    current_datetime = datetime.now()

                    purchase_day = current_datetime.day
                    purchase_month = current_datetime.month
                    conn = sqlite3.connect('shop.db')
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO analist (city, item, col, price, day, mont) VALUES (?, ?, ?, ?, ?, ?)",
                                   (city, item, gram, price_item, purchase_day,
                                    purchase_month))
                    conn.commit()
                    conn.close()
                    print("DAUN 2")
                    print(launge)
                    if launge == "ru":
                        print("DAUN 3")
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Локация 📍",
                                                     callback_data=f'_loc_clad_{latitude}_{longtitude}_{launge}')
                            ],

                            [
                                InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_clad, caption=f"Товар: {item}\n"
                                                                                       f"Граммовка: {gram}\n"
                                                                                       f"Цена: {price_item}\n"
                                                                                       f"Широта: {latitude}\n"
                                                                                       f"Долгота: {longtitude}",
                                             reply_markup=keyboard)

                    elif launge == "ua":
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Локація 📍",
                                                     callback_data=f'_loc_clad_{latitude}_{longtitude}_{launge}')
                            ],

                            [
                                InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_clad, caption=f"Товар: {item}\n"
                                                                                       f"Грамування: {gram}\n"
                                                                                       f"Ціна: {price_item}\n"
                                                                                       f"Широта: {latitude}\n"
                                                                                       f"Довгота: {longtitude}",
                                             reply_markup=keyboard)

                    elif launge == "en":
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Location 📍",
                                                     callback_data=f'_loc_clad_{latitude}_{longtitude}_{launge}')
                            ],

                            [
                                InlineKeyboardButton(text="Menu 💫", callback_data='back_menu_st_')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_clad, caption=f"Product: {item}\n"
                                                                                       f"Gram: {gram}\n"
                                                                                       f"Price: {price_item}\n"
                                                                                       f"Latitude: {latitude}\n"
                                                                                       f"Longitude: {longtitude}",
                                             reply_markup=keyboard)

                    elif launge == "pl":
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Lokalizacja 📍",
                                                     callback_data=f'_loc_clad_{latitude}_{longtitude}_{launge}')
                            ],

                            [
                                InlineKeyboardButton(text="Menu 💫", callback_data='back_menu_st_')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_clad, caption=f"Produkt: {item}\n"
                                                                                       f"Gram: {gram}\n"
                                                                                       f"Cena: {price_item}\n"
                                                                                       f"Szerokość geograficzna: {latitude}\n"
                                                                                       f"Długość geograficzna: {longtitude}",
                                             reply_markup=keyboard)

                    await bot.delete_message(call.message.chat.id, call.message.message_id)
                else:
                    if launge == "ru":
                        await bot.send_message(call.message.chat.id, "Ваш баланс недостаточный:",
                                               reply_markup=keyboard_cancel)
                        await bot.delete_message(call.message.chat.id, call.message.message_id)

                    elif launge == "ua":
                        await bot.send_message(call.message.chat.id, "Ваш баланс недостатній:",
                                               reply_markup=keyboard_cancel)
                        await bot.delete_message(call.message.chat.id, call.message.message_id)

                    elif launge == "en":
                        await bot.send_message(call.message.chat.id, "Your balance is insufficient:",
                                               reply_markup=keyboard_cancel)
                        await bot.delete_message(call.message.chat.id, call.message.message_id)

                    elif launge == "pl":
                        await bot.send_message(call.message.chat.id, "Twoje saldo jest niewystarczające:",
                                               reply_markup=keyboard_cancel)
                        await bot.delete_message(call.message.chat.id, call.message.message_id)

            else:
                if launge == "ru":
                    await bot.send_message(call.message.chat.id, "Ваш баланс недостаточный:",
                                           reply_markup=keyboard_cancel)
                    await bot.delete_message(call.message.chat.id, call.message.message_id)

                elif launge == "ua":
                    await bot.send_message(call.message.chat.id, "Ваш баланс недостатній:",
                                           reply_markup=keyboard_cancel)
                    await bot.delete_message(call.message.chat.id, call.message.message_id)

                elif launge == "en":
                    await bot.send_message(call.message.chat.id, "Your balance is insufficient:",
                                           reply_markup=keyboard_cancel)
                    await bot.delete_message(call.message.chat.id, call.message.message_id)

                elif launge == "pl":
                    await bot.send_message(call.message.chat.id, "Twoje saldo jest niewystarczające:",
                                           reply_markup=keyboard_cancel)
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
        else:
            if launge == "ru":
                await bot.send_message(call.message.chat.id, "Ваш баланс недостаточный:",
                                       reply_markup=keyboard_cancel)
                await bot.delete_message(call.message.chat.id, call.message.message_id)

            elif launge == "ua":
                await bot.send_message(call.message.chat.id, "Ваш баланс недостатній:",
                                       reply_markup=keyboard_cancel)
                await bot.delete_message(call.message.chat.id, call.message.message_id)

            elif launge == "en":
                await bot.send_message(call.message.chat.id, "Your balance is insufficient:",
                                       reply_markup=keyboard_cancel)
                await bot.delete_message(call.message.chat.id, call.message.message_id)

            elif launge == "pl":
                await bot.send_message(call.message.chat.id, "Twoje saldo jest niewystarczające:",
                                       reply_markup=keyboard_cancel)
                await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")