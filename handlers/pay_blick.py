from aiogram import Bot, types
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, PreCheckoutQuery)
import sqlite3
import aiohttp
from aiocryptopay import AioCryptoPay, Networks
import asyncio

import config
from utils.state import Asset_summ
from aiogram.types.message import ContentType

from aiogram.fsm.context import FSMContext
from utils.state import Blik, Blick_payment


async def blik_number(call: CallbackQuery, bot: Bot, state: FSMContext):
    launge = call.data.split('_')[2]
    await state.update_data(launge=launge)
    if launge == "ru":
        key = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')],
            [InlineKeyboardButton(text="Назад 🔙", callback_data=f'bliker_{launge}')]
        ])
        await bot.send_message(call.message.chat.id, "BLIK по Номеру (тел)/(счета) 📲\n\n"
                                                     "Введите сумму на которую хотите пополнить баланс.\n"
                                                     "Минимальное пополнение должно быть больше 30(zl).",
                               reply_markup=key)

    elif launge == "ua":
        key = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')],
            [InlineKeyboardButton(text="Назад 🔙", callback_data=f'bliker_{launge}')]
        ])
        await bot.send_message(call.message.chat.id, "BLIK по Номеру (тел)/(счета) 📲\n\n"
                                                     "Введите сумму на которую хотите пополнить баланс.\n"
                                                     "Минимальное пополнение должно быть больше 30(zl).",
                               reply_markup=key)
    elif launge == "en":
        key = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')],
            [InlineKeyboardButton(text="Назад 🔙", callback_data=f'bliker_{launge}')]
        ])
        await bot.send_message(call.message.chat.id, "BLIK по Номеру (тел)/(счета) 📲\n\n"
                                                     "Введите сумму на которую хотите пополнить баланс.\n"
                                                     "Минимальное пополнение должно быть больше 30(zl).",
                               reply_markup=key)
    elif launge == "pl":
        key = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')],
            [InlineKeyboardButton(text="Назад 🔙", callback_data=f'bliker_{launge}')]
        ])
        await bot.send_message(call.message.chat.id, "BLIK по Номеру (тел)/(счета) 📲\n\n"
                                                     "Введите сумму на которую хотите пополнить баланс.\n"
                                                     "Минимальное пополнение должно быть больше 30(zl).",
                               reply_markup=key)

    await state.set_state(Blick_payment.summ_blick)

    await bot.delete_message(call.message.chat.id, call.message.message_id)




async def blik_number_end(message:  Message, bot: Bot, state: FSMContext):
    try:
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM blik ORDER BY id DESC")
        rows = cursor.fetchall()
        number_iban = ""
        number_phone = ""
        name = ""
        for row in rows:
            number_iban = row[1]
            number_phone = row[2]
            name = row[3]
            print(row)
        conn.close()
        ru = "ru"
        print("huis")
        price = message.text
        print(price)
        name_user = message.from_user.username
        external_id = message.chat.id
        await bot.delete_message(message.chat.id, message.message_id - 1)
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM check_def WHERE external_id = ?", (external_id,))
        existing_record = cursor.fetchone()
        keys = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Назад 🔙", callback_data='blik_number')
            ]
        ])
        if not price.isdigit():

            await bot.send_message(message.chat.id, "Сумма должна быть числом.",
                                   reply_markup=keys)
            await bot.delete_message(message.chat.id, message.message_id)
        else:
            inter_price = int(price)
            if inter_price < 30:
                await bot.send_message(message.chat.id, "Сумма чека должна быть больше 30 zl.",
                                       reply_markup=keys)
                await bot.delete_message(message.chat.id, message.message_id)
            else:
                if existing_record:
                    cursor.execute("SELECT number_check FROM check_def WHERE external_id = ?", (external_id,))
                    number_of_checks = cursor.fetchone()[0]
                    print(number_of_checks)
                    if number_of_checks < 10:
                        cursor.execute("UPDATE check_def SET number_check = number_check + 1 WHERE external_id = ?",
                                       (external_id,))
                        conn.commit()
                        cursor.execute("SELECT number_check FROM check_def WHERE external_id = ?", (external_id,))
                        number_check = cursor.fetchone()[0]
                        cursor.execute(
                            "INSERT INTO cheker (number_check, external_id, name_user, price) VALUES (?, ?, ?, ?)",
                            (number_check, external_id, name_user, price))
                        key = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Подтвердить ✅",callback_data=f'_buy_check_{number_check}_{price}')
                            ],
                            [
                                InlineKeyboardButton(text="Удалить 🗑", callback_data=f'_del_check_{number_check}_{price}')
                            ],
                            [
                                InlineKeyboardButton(text="Меню 💫", callback_data=f'back_menu_st_{ru}'),
                                InlineKeyboardButton(text="Назад 🔙", callback_data=f'balance_user_{ru}')
                            ]

                        ])
                        await bot.send_message(message.chat.id, f"BLIK ЧЕК 📲#{number_check}\n\n"
                                                                f"Номер счета:\n"
                                                                f"{number_iban}\n\n"
                                                                "Номер телефона:\n"
                                                                f"{number_phone}\n\n"
                                                                f"Имя получателя: {name}\n"
                                                                "Описание перевода: Podarunok\n\n"
                                                                f"Ваш id:({external_id})\n"
                                                                f"Сумма платежа:{price} zl\n"
                                                                f"Статус платежа: Ожидает оплаты.",
                                               reply_markup=key)
                        await bot.delete_message(message.chat.id, message.message_id)
                        conn.commit()
                        conn.close()

                    else:
                        key = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Активные чеки 🧾", callback_data='_check_act_')
                            ],
                            [
                                InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st'),
                                InlineKeyboardButton(text="Назад 🔙", callback_data='balance_user')
                            ]
                        ])
                        await bot.send_message(message.chat.id, "У вас уже есть 4 активных чека.\n"
                                                                "Удалите или оплатите их.\n"
                                                                "Чтоб удалить или оплатить их перейдите в Активные чеки 🧾",
                                               reply_markup=key)

                        await bot.delete_message(message.chat.id, message.message_id)
                else:
                    cursor.execute("INSERT INTO check_def (number_check, external_id) VALUES (?, ?)", (0, external_id))
                    number_check = 1
                    cursor.execute(
                        "INSERT INTO cheker (number_check, external_id, name_user, price) VALUES (?, ?, ?, ?)",
                        (number_check, external_id, name_user, price))
                    keysd = InlineKeyboardMarkup(inline_keyboard=[

                        [
                            InlineKeyboardButton(text="Подтвердить ✅",callback_data=f'_buy_check_{number_check}_{price}')
                        ],
                        [
                            InlineKeyboardButton(text="Удалить 🗑", callback_data=f'_del_check_{number_check}_{price}')
                        ],
                        [
                            InlineKeyboardButton(text="Меню 💫", callback_data=f'back_menu_st_{ru}'),
                            InlineKeyboardButton(text="Назад 🔙", callback_data=f'blik_number_{ru}')
                        ]
                    ])


                    await bot.send_message(message.chat.id, f"BLIK ЧЕК 📲#{number_check}\n\n"
                                                                f"Номер счета:\n"
                                                                f"{number_iban}\n\n"
                                                                "Номер телефона:\n"
                                                                f"{number_phone}\n\n"
                                                                f"Имя получателя: {name}\n"
                                                                "Описание перевода: Podarunok\n\n"
                                                                f"Ваш id:({external_id})\n"
                                                                f"Сумма платежа:{price} zl\n"
                                                                f"Статус платежа: Ожидает оплаты.",
                                           reply_markup=keysd)
                    await bot.delete_message(message.chat.id, message.message_id)
                    conn.commit()
                    conn.close()
    except Exception as e:
        print(repr(e))


async def del_check_end(call: CallbackQuery, bot: Bot):
    try:
        number_check = call.data.split('_')[3]
        price = call.data.split('_')[4]
        external_id = call.message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM blik ORDER BY id DESC")
        rows = cursor.fetchall()
        number_iban = ""
        number_phone = ""
        name = ""
        for row in rows:
            number_iban = row[1]
            number_phone = row[2]
            name = row[3]
            print(row)
        conn.close()

        key = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Подтвердить ✅", callback_data=f'_end_check_{number_check}'),
                InlineKeyboardButton(text="Отмена ❌", callback_data=f'_can_ch_{number_check}_{price}_')
            ]
        ])


        await bot.send_message(call.message.chat.id, f"BLIK ЧЕК 📲#{number_check}\n\n"
                                                     f"Номер счета:\n"
                                                     f"{number_iban}\n\n"
                                                     "Номер телефона:\n"
                                                     f"{number_phone}\n\n"
                                                     f"Имя получателя: {name}\n"
                                                     "Описание перевода: Podarunok\n\n"
                                                     f"Сумма платежа: {price} zl\n"
                                                     f"Ваш id: ({external_id})\n"
                                                     f"Статус платежа: Ожидает оплаты.\n\n"
                                                     f"Вы действительно хотите удалить чек?", reply_markup=key)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass


async def can_check_call(call: CallbackQuery, bot: Bot):
    number_check = call.data.split('_')[3]
    price = call.data.split('_')[4]
    external_id = call.message.chat.id
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM blik ORDER BY id DESC")
    rows = cursor.fetchall()
    number_iban = ""
    number_phone = ""
    name = ""
    for row in rows:
        number_iban = row[1]
        number_phone = row[2]
        name = row[3]
        print(row)
    conn.close()
    ru = "ru"
    key = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Подтвердить ✅", callback_data=f'_end_check_{number_check}'),
        ],
        [
            InlineKeyboardButton(text="Отмена ❌", callback_data=f'_can_ch_{number_check}_{price}_')
        ],
        [
            InlineKeyboardButton(text="Меню 💫", callback_data=f'back_menu_st_{ru}'),
            InlineKeyboardButton(text="Назад 🔙", callback_data=f'blik_number_{ru}')
        ]
    ])

    await bot.send_message(call.message.chat.id, f"BLIK ЧЕК 📲#{number_check}\n\n"
                                           f"Номер счета:\n"
                                           f"{number_iban}\n\n"
                                           "Номер телефона:\n"
                                           f"{number_phone}\n\n"
                                           f"Имя получателя: {name}\n"
                                           "Описание перевода: Podarunok\n\n"
                                           f"Ваш id: ({external_id})\n"
                                           f"Сумма платежа: {price} zl\n"
                                           f"Статус платежа: Ожидает оплаты.", reply_markup=key)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


async def end_check(call: CallbackQuery, bot: Bot):
    number_check = call.data.split('_')[3]
    external_id = call.message.chat.id
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM cheker WHERE external_id = ? AND number_check = ?",
                   (external_id, number_check))

    # Записываем изменения в базу данных
    conn.commit()

    # Закрываем соединение с базой данных
    conn.close()
    ru = "ru"
    key = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Меню 💫", callback_data=f'back_menu_st_{ru}')
        ]
    ])

    await bot.send_message(call.message.chat.id, "Удаление 🗑\n"
                                                 "Ваш чек успешно удалён.", reply_markup=key)

    await bot.delete_message(call.message.chat.id, call.message.message_id)



async def buy_check_photo(call: CallbackQuery, bot: Bot, state: FSMContext):
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM blik ORDER BY id DESC")
    rows = cursor.fetchall()
    number_iban = ""
    number_phone = ""
    name = ""
    for row in rows:
        number_iban = row[1]
        number_phone = row[2]
        name = row[3]
        print(row)
    conn.close()
    number_check = call.data.split('_')[3]
    price = call.data.split('_')[4]
    user_id = call.message.chat.id
    key = InlineKeyboardMarkup(inline_keyboard=[
        [
                InlineKeyboardButton(text="Назад 🔙", callback_data=f'_can_ch_{number_check}_{price}')
        ]
    ])
    await state.set_state(Blick_payment.check_end)

    await bot.send_message(call.message.chat.id, f"Подтверждение оплаты ✅"
                                                 f"BLIK ЧЕК 📲#{number_check}\n\n"
                                                 f"Номер счета:\n"
                                                 f"{number_iban}\n\n"
                                                 "Номер телефона:\n"
                                                 f"{number_phone}\n\n"
                                                 f"Имя получателя: {name}\n"
                                                 "Описание перевода: Podarunok\n\n"
                                                 f"Сумма платежа: {price} zl\n"
                                                 f"Ваш id: ({user_id})\n"
                                                 f"Статус платежа: Ожидает оплаты.\n\n"
                                                 f"Отправьте фотографию чека:", reply_markup=key)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await state.update_data(price=price)
    await state.update_data(number_check=number_check)




async def buy_check_end(message: Message, bot: Bot, state: FSMContext):
    name_user = message.from_user.username
    external_id = message.chat.id
    context_data = await state.get_data()
    price = context_data.get('price')
    number_check = context_data.get('number_check')

    if message.photo:
        photo_url = message.photo[-1].file_id
    else:
        photo_url = None
    await bot.delete_message(message.chat.id, message.message_id - 1)

    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cheker_conf (number_check, external_id, name_user, price, photo_check) VALUES (?, ?, ?, ?, ?)",
        (number_check, external_id, name_user, price, photo_url))
    conn.commit()
    conn.close()
    key = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Выйти 🔙", callback_data=f'back_menu_st_')
        ]
    ])

    await bot.send_message(message.chat.id,
                     f"Ваш чек на расмотрении.\nВ течение 5-30 минут ваш баланс обновиться.\nСтатус чека можно посмотреть в кнопке (Активные чеки 🧾)",
                     reply_markup=key)
    await bot.delete_message(message.chat.id, message.message_id)

