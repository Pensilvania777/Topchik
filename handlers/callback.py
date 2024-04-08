from aiogram import Bot
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
import sqlite3
from aiogram.fsm.context import FSMContext
from config import BOT_NAME
from utils.state import Comment, Dispute
import pyperclip


async def buy_insert(call: CallbackQuery, bot: Bot):
    try:
        result = call.data.split('_')[2]
        if result == "ru":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Покупка 🛍", callback_data='buy_ins')],
                [InlineKeyboardButton(text="Клад 🧲", callback_data=f'buy_clad_{result}')],
                [InlineKeyboardButton(text="Назад 🔙", callback_data=f'back_menu_st_')],
            ])
            await bot.send_message(call.message.chat.id, "Выберите способ покупки", reply_markup=keyboard)
        elif result == "ua":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Покупка 🛍", callback_data='buy_ins')],
                [InlineKeyboardButton(text="Клад 🧲", callback_data=f'buy_clad_{result}')],
                [InlineKeyboardButton(text="Назад 🔙", callback_data=f'back_menu_st_')],
            ])
            await bot.send_message(call.message.chat.id, "Виберіть спосіб покупки", reply_markup=keyboard)
        elif result == "en":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Purchase 🛍", callback_data='buy_ins')],
                [InlineKeyboardButton(text="Treasure 🧲", callback_data=f'buy_clad_{result}')],
                [InlineKeyboardButton(text="Back 🔙", callback_data=f'back_menu_st_')],
            ])
            await bot.send_message(call.message.chat.id, "Choose a purchase method", reply_markup=keyboard)
        elif result == "pl":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Zakup 🛍", callback_data='buy_ins')],
                [InlineKeyboardButton(text="Skarb 🧲", callback_data=f'buy_clad_{result}')],
                [InlineKeyboardButton(text="Z powrotem 🔙", callback_data=f'back_menu_st_')],

            ])
            await bot.send_message(call.message.chat.id, "Wybierz metodę zakupu", reply_markup=keyboard)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass


async def return_start(call: CallbackQuery, bot: Bot):
    try:
        user_id = call.message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT launge_user FROM users_shop WHERE external_id = ?", (user_id,))
        resul = cursor.fetchone()
        conn.close()
        result = str(resul[0])

        if result == "ru":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Покупка 🛍", callback_data=f'buy_ins_{result}')],
                [InlineKeyboardButton(text="Мой аккаунт 👨‍🏫", callback_data=f'my_acc_{result}')],

                [
                    InlineKeyboardButton(text="Язык 🌍", callback_data=f'language_{result}'),
                    InlineKeyboardButton(text="Комментарии 📨", callback_data=f'comview_{result}')
                ],
                [
                    InlineKeyboardButton(text="Правила 📑", callback_data=f'faq_{result}'),
                    InlineKeyboardButton(text="Инструкция 📋", callback_data=f'instruction_{result}')
                ],
            ])
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT text_menu, photo_menu FROM oform_ru WHERE id = ?''', (1,))

            result = cursor.fetchone()
            photo_menu = ""
            text_menu = ""
            if result:
                text_menu, photo_menu = result
            conn.close()
            await bot.send_photo(call.message.chat.id, photo_menu, caption=text_menu, reply_markup=keyboard)

        elif result == "ua":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Покупка 🛍", callback_data=f'buy_ins_{result}')],
                [InlineKeyboardButton(text="Мій аккаунт 👨‍🏫", callback_data=f'my_acc_{result}')],
                [
                    InlineKeyboardButton(text="Мова 🌍", callback_data=f'language_{result}'),
                    InlineKeyboardButton(text="Комментарии 📨", callback_data=f'comview_{result}')
                ],
                [
                    InlineKeyboardButton(text="Інструкція 📋", callback_data=f'instruction_{result}'),
                    InlineKeyboardButton(text="Правила 📑", callback_data=f'faq_{result}')
                ],

            ])
            await bot.send_message(call.message.chat.id, "Бот автопродаж 🏪", reply_markup=keyboard)
        elif result == "en":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Purchase 🛍", callback_data=f'buy_ins_{result}')],
                [InlineKeyboardButton(text="My account 👨‍🏫", callback_data=f'my_acc_{result}')],
                [
                    InlineKeyboardButton(text="Language 🌍", callback_data=f'language_{result}'),
                    InlineKeyboardButton(text="Comment 📨", callback_data=f'comview_{result}')

                ],
                [

                    InlineKeyboardButton(text="Rules 📑", callback_data=f'faq_{result}'),
                    InlineKeyboardButton(text="Instructions 📋", callback_data=f'instruction_{result}')

                ]

            ])
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT text_menu, photo_menu FROM oform_en WHERE id = ?''', (1,))

            result = cursor.fetchone()
            photo_menu = ""
            text_menu = ""
            if result:
                text_menu, photo_menu = result
            conn.close()
            await bot.send_photo(call.message.chat.id, photo_menu, caption=text_menu, reply_markup=keyboard)

        elif result == "pl":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Zakup 🛍", callback_data=f'buy_ins_{result}')],
                [InlineKeyboardButton(text="Moje konto 👨‍🏫", callback_data=f'my_acc_{result}')],
                [
                    InlineKeyboardButton(text="Język 🌍", callback_data=f'language_{result}'),
                    InlineKeyboardButton(text="Comment 📨", callback_data=f'comview_{result}')

                ],
                [
                    InlineKeyboardButton(text="Instrukcje 📋", callback_data=f'instruction_{result}'),
                    InlineKeyboardButton(text="Zasady 📑", callback_data=f'faq_{result}')
                ],

            ])
            await bot.send_message(call.message.chat.id, "Bot sprzedaży automatycznej 🏪", reply_markup=keyboard)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(e)


async def language(call: CallbackQuery, bot: Bot):
    try:
        ru = "ru"
        ua = "ua"
        en = "en"
        pl = "pl"
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT text_menu, photo_menu FROM oform_ru WHERE id = ?''', (1,))

        result = cursor.fetchone()
        text_menu = ""
        photo_menu = ""
        if result:
            text_menu, photo_menu = result
        conn.close()
        key_language = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Русский 🇷🇺", callback_data=f'laungeuage_set_{ru}')],
            [InlineKeyboardButton(text="Український 🇺🇦", callback_data=f'laungeuage_set_{ua}')],
            [InlineKeyboardButton(text="English 🇬🇧", callback_data=f'laungeuage_set_{en}')],
            [InlineKeyboardButton(text="Polski 🇵🇱", callback_data=f'laungeuage_set_{pl}')],
            [InlineKeyboardButton(text="Назад 🔙", callback_data=f'back_menu_st_')]

        ])
        await bot.send_photo(call.message.chat.id, photo_menu, caption=text_menu, reply_markup=key_language)

        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(e)


async def comment_run(call: CallbackQuery, bot: Bot):
    comment_id = 1
    await comment_view(call.message, bot, comment_id)


async def comment_view(message: Message, bot: Bot, comment_id):
    try:
        limit = 1
        offset = 0
        chat_id = message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()

        # Извлекаем комментарии из базы данных с использованием LIMIT и OFFSET
        cursor.execute("SELECT * FROM comment WHERE id = ? LIMIT 1 OFFSET ?", (comment_id, offset))
        comments = cursor.fetchall()

        # Закрываем соединение
        conn.close()

        if comments:
            for comment in comments:
                text = f"Текст комментария: {comment[1]}\nОценка: {comment[2]}\nID пользователя: {comment[3]}\nТовар: {comment[4]}\nГрамм: {comment[5]}"

                # Создаем клавиатуру с кнопками "назад" и "вперед"
                key_language = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="⬅️", callback_data=f"prev {comment[0]}"),
                        InlineKeyboardButton(text="➡️", callback_data=f"next {comment[0]}")

                    ],
                    [
                        InlineKeyboardButton(text="Выйти", callback_data="back_menu_st_")
                    ]
                ])
                await bot.send_message(chat_id, text, reply_markup=key_language)
        else:
            key_language = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Comment 📨", callback_data=f'comview_')
                ]
            ])
            await bot.send_message(chat_id, "Нет комментариев.", reply_markup=key_language)
        await bot.delete_message(message.chat.id, message.message_id)
    except:
        pass


# Обработчик нажатий на кнопки InlineKeyboard
async def process_callback(call: CallbackQuery, bot: Bot):
    try:
        data = call.data.split()
        command = data[0]
        comment_id = int(data[1])

        if command == "next":
            await comment_view(call.message, bot, comment_id + 1)
        elif command == "prev":
            await comment_view(call.message, bot, comment_id - 1)
    except:
        pass


async def language_end(call: CallbackQuery, bot: Bot):
    try:
        language = call.data.split('_')[2]

        user_id = call.message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()

        # Обновление значения launge_user для заданного external_id
        cursor.execute("UPDATE users_shop SET launge_user = ? WHERE external_id = ?", (language, user_id))

        # Применение изменений и закрытие соединения
        conn.commit()
        conn.close()
        key_language = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Назад 🔙", callback_data=f'back_menu_st_')]
        ])

        if language == "ru":
            await bot.send_message(call.message.chat.id, "Язык установлен", reply_markup=key_language)
        elif language == "ua":
            await bot.send_message(call.message.chat.id, "Мову встановлено", reply_markup=key_language)
        elif language == "en":
            await bot.send_message(call.message.chat.id, "Language set", reply_markup=key_language)
        elif language == "pl":
            await bot.send_message(call.message.chat.id, "Jezyk ustawiony", reply_markup=key_language)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass


async def my_acc(call: CallbackQuery, bot: Bot):
    try:
        result = call.data.split('_')[2]
        user_id = call.message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users_shop WHERE external_id=?", (user_id,))
        users = cursor.fetchall()
        conn.close()
        external_id = ""
        balance = ""
        col_buy = ""
        open_dispute = ""
        close_dispute = ""
        language_set = ""
        for user in users:
            id, name_user, external_id, language_set, balance, col_buy, open_dispute, close_dispute = user

        if result == "ru":

            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Копировать ID", callback_data=f'copy_text_')],
                [InlineKeyboardButton(text="История покупок 🗂", callback_data=f'history_buy_{result}')],
                [InlineKeyboardButton(text="Баланс ➕", callback_data=f'balance_user_{result}')],
                [InlineKeyboardButton(text="Реферальная система 👥", callback_data=f'reffer_system_{result}')],
                [InlineKeyboardButton(text="Назад 🔙", callback_data='back_menu_st_')]
            ])
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT text_profile, photo_profile FROM oform_ru WHERE id = ?''', (1,))

            result = cursor.fetchone()
            photo_menu = ""
            if result:
                text_menu, photo_menu = result
            conn.close()
            await bot.send_photo(call.message.chat.id, photo_menu, caption="Мой аккаунт 👨‍🏫\n\n"
                                                                           f"Ваш external id: {external_id}\n"
                                                                           f"Баланс : {balance}zl\n"
                                                                           f"Количество покупок : {col_buy}\n\n"
                                                                           f"Открытые споры : {open_dispute}\n"
                                                                           f"Закрытые споры : {close_dispute}\n\n"
                                                                           f"Язык : {language_set}\n",
                                 reply_markup=keyboard)

        elif result == "ua":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Історія покупок 🗂", callback_data=f'history_buy_{result}')],
                [InlineKeyboardButton(text="Баланс ➕", callback_data=f'balance_user_{result}')],
                [InlineKeyboardButton(text="Реферальна система 👥", callback_data=f'reffer_system_{result}')],
                [InlineKeyboardButton(text="Назад 🔙", callback_data='back_menu_st_')]
            ])
            await bot.send_message(call.message.chat.id, "Мiй аккаунт 👨‍🏫\n\n"
                                                         f"Ваш external id: {external_id}\n"
                                                         f"Баланс : {balance}zl\n"
                                                         f"Кількість покупок : {col_buy}\n\n"
                                                         f"Відкриті суперечки : {open_dispute}\n"
                                                         f"Закриті суперечки : {close_dispute}\n\n"
                                                         f"Мова : {language_set}\n"
                                   , reply_markup=keyboard)
        elif result == "en":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Purchase history 🗂", callback_data=f'history_buy_{result}')],
                [InlineKeyboardButton(text="Balance ➕", callback_data=f'balance_user_{result}')],
                [InlineKeyboardButton(text="Referral system 👥", callback_data=f'reffer_system_{result}')],
                [InlineKeyboardButton(text="Back 🔙", callback_data='back_menu_st_')]
            ])
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT text_profile, photo_profile FROM oform_en WHERE id = ?''', (1,))

            result = cursor.fetchone()
            photo_menu = ""
            if result:
                text_menu, photo_menu = result
            conn.close()
            await bot.send_photo(call.message.chat.id, photo_menu, caption="My account 👨‍🏫\n\n"
                                                         f"Your external id: {external_id}\n"
                                                         f"Balance : {balance}zl\n"
                                                         f"Number of purchases : {col_buy}\n\n"
                                                         f"Open disputes : {open_dispute}\n"
                                                         f"Closed disputes : {close_dispute}\n\n"
                                                         f"Language : {language_set}\n",
                                 reply_markup=keyboard)


        elif result == "pl":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Historia zakupów 🗂", callback_data=f'history_buy_{result}')],
                [InlineKeyboardButton(text="Balansować ➕", callback_data=f'balance_user_{result}')],
                [InlineKeyboardButton(text="System skierowania 👥", callback_data=f'reffer_system_{result}')],
                [InlineKeyboardButton(text="Z powrotem 🔙", callback_data='back_menu_st_')]
            ])
            await bot.send_message(call.message.chat.id, "Moje konto 👨‍🏫\n\n"
                                                         f"Twój identyfikator zewnętrzny: {external_id}\n"
                                                         f"Balansować : {balance}zl\n"
                                                         f"Liczba zakupów : {col_buy}\n\n"
                                                         f"Otwarte spory : {open_dispute}\n"
                                                         f"Zamknięte spory : {close_dispute}\n\n"
                                                         f"Język : {language_set}\n"
                                   , reply_markup=keyboard)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(repr(e))


async def copy_text(call: CallbackQuery, bot: Bot):
    try:
        copied_text = call.message.chat.id
        pyperclip.copy(copied_text)  # Копируем текст в буфер обмена
        await call.answer('Ваш ID скопирован', show_alert=True)
    except Exception as e:
        print(repr(e))


async def reffer_system(call: CallbackQuery, bot: Bot):
    try:
        launge = call.data.split('_')[2]
        user_id = call.message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*), SUM(col_sale) FROM refferrss WHERE reffer_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        if launge == "ru":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Назад 🔙", callback_data=f'my_acc_{launge}')]
            ])
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT text_reff, photo_reff FROM oform_ru WHERE id = ?''', (1,))

            okey = cursor.fetchone()
            text_menu = ""
            photo_menu = ""
            if okey:
                text_menu, photo_menu = okey
            conn.close()
            await bot.send_photo(call.message.chat.id, photo=photo_menu,
                                 caption=f"Количество присоединенных рефералов: {result[0]}\n"
                                         f"Количество скидок на 10% при покупке: {result[1]}\n"
                                         f"https://t.me/{BOT_NAME}?start={user_id}\n"
                                         f"", reply_markup=keyboard)
        elif launge == "ua":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Назад 🔙", callback_data=f'my_acc_{launge}')]
            ])
            await bot.send_message(call.message.chat.id, f"Кількість приєднаних рефералів: {result[0]}\n"
                                                         f"Кількість знижок на 10% при покупці: {result[1]}\n"
                                                         f"https://t.me/{BOT_NAME}?start={user_id}\n"
                                                         f"", reply_markup=keyboard)

        elif launge == "en":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Back 🔙", callback_data=f'my_acc_{launge}')]
            ])
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT text_reff, photo_reff FROM oform_en WHERE id = ?''', (1,))

            okey = cursor.fetchone()
            text_menu = ""
            photo_menu = ""
            if okey:
                text_menu, photo_menu = okey
            conn.close()
            await bot.send_photo(call.message.chat.id, photo=photo_menu,
                                 caption=f"Number of connected referrals: {result[0]}\n"
                                                         f"Number of 10% discounts on purchase: {result[1]}\n"
                                                         f"https://t.me/{BOT_NAME}?start={user_id}\n"
                                                         f"", reply_markup=keyboard)


        elif launge == "pl":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Z powrotem 🔙", callback_data=f'my_acc_{launge}')]
            ])
            await bot.send_message(call.message.chat.id, f"Liczba połączonych poleceń: {result[0]}\n"
                                                         f"Liczba 10% rabatów na zakup: {result[1]}\n"
                                                         f"https://t.me/{BOT_NAME}?start={user_id}\n"
                                                         f"", reply_markup=keyboard)

        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(repr(e))


async def balance_user(call: CallbackQuery, bot: Bot):
    try:
        launge = call.data.split('_')[2]

        if launge == "ru":
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT text_banc, photo_banc FROM oform_ru WHERE id = ?''', (1,))

            result = cursor.fetchone()
            text_menu = ""
            photo_menu = ""
            if result:
                text_menu, photo_menu = result
            conn.close()
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Активные чеки 🧾", callback_data=f'_active_check_{launge}'),
                    InlineKeyboardButton(text="Инструкция 📄", callback_data=f'blik_instuc_{launge}')
                ],
                [
                    InlineKeyboardButton(text="BLIK 📲", callback_data=f'bliker_{launge}'),
                    InlineKeyboardButton(text="Криптовалюта 🪙", callback_data=f'crypto_{launge}')
                ],

                [InlineKeyboardButton(text="Меню 💫", callback_data=f'back_menu_st_{launge}'),
                 InlineKeyboardButton(text="Назад 🔙", callback_data=f'my_acc_{launge}')]
            ])
            await bot.send_photo(call.message.chat.id, photo_menu, caption=text_menu, reply_markup=keyboard)

        elif launge == "ua":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Активні чеки 🧾", callback_data=f'_active_check_{launge}'),
                    InlineKeyboardButton(text="Інструкція 📄", callback_data=f'blik_instuc_{launge}')
                ],
                [
                    InlineKeyboardButton(text="BLIK 📲", callback_data=f'bliker_{launge}'),
                    InlineKeyboardButton(text="Криптовалюта 🪙", callback_data=f'crypto_{launge}')
                ],

                [InlineKeyboardButton(text="Меню 💫", callback_data=f'back_menu_st_{launge}'),
                 InlineKeyboardButton(text="Назад 🔙", callback_data=f'my_acc_{launge}')]
            ])
            await bot.send_message(call.message.chat.id, "Пополнение Баланса ➕", reply_markup=keyboard)

        elif launge == "en":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Active checks 🧾", callback_data=f'_active_check_{launge}'),
                    InlineKeyboardButton(text="Instructions 📄", callback_data=f'blik_instuc_{launge}')
                ],
                [
                    InlineKeyboardButton(text="BLIK 📲", callback_data=f'bliker_{launge}'),
                    InlineKeyboardButton(text="Cryptocurrency 🪙", callback_data=f'crypto_{launge}')
                ],

                [InlineKeyboardButton(text="Menu 💫", callback_data=f'back_menu_st_{launge}'),
                 InlineKeyboardButton(text="Back 🔙", callback_data=f'my_acc_{launge}')]
            ])
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT text_banc, photo_banc FROM oform_en WHERE id = ?''', (1,))

            result = cursor.fetchone()
            text_menu = ""
            photo_menu = ""
            if result:
                text_menu, photo_menu = result
            conn.close()
            await bot.send_photo(call.message.chat.id, photo_menu, caption=text_menu, reply_markup=keyboard)

        elif launge == "pl":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Aktywne kontrole 🧾", callback_data=f'_active_check_{launge}'),
                    InlineKeyboardButton(text="Instrukcje 📄", callback_data=f'blik_instuc_{launge}')
                ],
                [
                    InlineKeyboardButton(text="BLIK 📲", callback_data=f'bliker_{launge}'),
                    InlineKeyboardButton(text="Kryptowaluta 🪙", callback_data=f'crypto_{launge}')
                ],

                [InlineKeyboardButton(text="Menu 💫", callback_data=f'back_menu_st_{launge}'),
                 InlineKeyboardButton(text="Z powrotem 🔙", callback_data=f'my_acc_{launge}')]
            ])
            await bot.send_message(call.message.chat.id, "Пополнение Баланса ➕", reply_markup=keyboard)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass


async def history_buy(call: CallbackQuery, bot: Bot):
    try:
        user_id = call.message.chat.id
        launge = call.data.split('_')[2]
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        external_id = call.from_user.id
        cursor.execute("SELECT id FROM active_clad WHERE external_id = ?", (external_id,))
        ids = cursor.fetchall()
        conn.close()

        if launge == "ru":

            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT text_izbpokup, photo_izbpokup FROM oform_ru WHERE id = ?''', (1,))

            result = cursor.fetchone()
            text_menu = ""
            photo_menu = ""
            if result:
                text_menu, photo_menu = result
            conn.close()
            if len(ids) == 0:
                key_city = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Назад", callback_data=f'my_acc_{launge}')
                    ]

                ])
                await bot.send_photo(user_id, photo_menu, caption="Нет доступных покупок.", reply_markup=key_city)
                await bot.delete_message(user_id, call.message.message_id)
            else:
                key_city = InlineKeyboardMarkup(inline_keyboard=[])

                for i in range(0, len(ids), 2):
                    row = []
                    if i < len(ids) - 1:
                        row.append(InlineKeyboardButton(text=str(ids[i][0]),
                                                        callback_data=f'_view_item_{ids[i][0]}__{launge}'))
                        row.append(
                            InlineKeyboardButton(text=str(ids[i + 1][0]),
                                                 callback_data=f'_view_item_{ids[i + 1][0]}__{launge}'))
                    else:
                        row.append(InlineKeyboardButton(text=str(ids[i][0]),
                                                        callback_data=f'_view_item_{ids[i][0]}__{launge}'))
                    key_city.inline_keyboard.append(row)

                key_city.inline_keyboard.append([
                    InlineKeyboardButton(text="Назад", callback_data=f'my_acc_{launge}')
                ])
                await bot.send_photo(user_id, photo_menu, caption=text_menu, reply_markup=key_city)

        elif launge == "ua":
            if len(ids) == 0:
                key_city = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Назад", callback_data=f'my_acc_{launge}')
                    ]

                ])
                await bot.send_message(user_id, "Нет доступных покупок.", reply_markup=key_city)
                await bot.delete_message(user_id, call.message.message_id)
            else:
                key_city = InlineKeyboardMarkup(inline_keyboard=[])

                for i in range(0, len(ids), 2):
                    row = []
                    if i < len(ids) - 1:
                        row.append(
                            InlineKeyboardButton(text=ids[i][0], callback_data=f'_view_item_{ids[i][0]}__{launge}'))
                        row.append(
                            InlineKeyboardButton(text=ids[i + 1][0],
                                                 callback_data=f'_view_item_{ids[i + 1][0]}__{launge}'))
                    else:
                        row.append(
                            InlineKeyboardButton(text=ids[i][0], callback_data=f'_view_item_{ids[i][0]}__{launge}'))
                    key_city.inline_keyboard.append(row)

                key_city.inline_keyboard.append([
                    InlineKeyboardButton(text="Назад", callback_data=f'my_acc_{launge}')
                ])
                await bot.send_message(call.message.chat.id, "Історія покупок 🗂\nВиберіть покупку:",
                                       reply_markup=key_city)

        elif launge == "en":
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT text_izbpokup, photo_izbpokup FROM oform_en WHERE id = ?''', (1,))

            result = cursor.fetchone()
            text_menu = ""
            photo_menu = ""
            if result:
                text_menu, photo_menu = result
            conn.close()
            if len(ids) == 0:
                key_city = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Назад", callback_data=f'my_acc_{launge}')
                    ]

                ])
                await bot.send_message(user_id, "Нет доступных покупок.", reply_markup=key_city)
                await bot.delete_message(user_id, call.message.message_id)
            else:
                key_city = InlineKeyboardMarkup(inline_keyboard=[])

                for i in range(0, len(ids), 2):
                    row = []
                    if i < len(ids) - 1:
                        row.append(
                            InlineKeyboardButton(text=ids[i][0], callback_data=f'_view_item_{ids[i][0]}__{launge}'))
                        row.append(
                            InlineKeyboardButton(text=ids[i + 1][0],
                                                 callback_data=f'_view_item_{ids[i + 1][0]}__{launge}'))
                    else:
                        row.append(
                            InlineKeyboardButton(text=ids[i][0], callback_data=f'_view_item_{ids[i][0]}__{launge}'))
                    key_city.inline_keyboard.append(row)

                key_city.inline_keyboard.append([
                    InlineKeyboardButton(text="Назад", callback_data=f'my_acc_{launge}')
                ])
                await bot.send_photo(user_id, photo_menu, caption=text_menu, reply_markup=key_city)


        elif launge == "pl":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=f'ID: {record[0]}', callback_data=f'_view_item_{record[0]}__{launge}') for
                 record
                 in ids],
                [InlineKeyboardButton(text="Z powrotem 🔙", callback_data=f'my_acc_{launge}')],
            ])
            await bot.send_message(call.message.chat.id, "Historia zakupów 🗂\n\nWybierz zakup:", reply_markup=keyboard)

        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(repr(e))


async def active_check(call: CallbackQuery, bot: Bot):
    try:
        launge = call.data.split('_')[3]
        user_id = call.message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()

        # Выполняем запрос к базе данных, чтобы получить прайс для заданного external_id
        cursor.execute("SELECT number_check FROM cheker_conf WHERE external_id = ?", (user_id,))
        results = cursor.fetchall()

        if len(results) == 0:
            if launge == "ru":
                message = "Нет активных чеков"
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Меню 💫", callback_data=f'back_menu_st_{launge}')],
                    [InlineKeyboardButton(text="Назад 🔙", callback_data=f'balance_user_{launge}')]
                ])
                await bot.send_message(chat_id=user_id, text=message, reply_markup=keyboard)

            elif launge == "ua":
                message = "Немає активних чеків"
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Меню 💫", callback_data=f'back_menu_st_{launge}')],
                    [InlineKeyboardButton(text="Назад 🔙", callback_data=f'balance_user_{launge}')]
                ])
                await bot.send_message(chat_id=user_id, text=message, reply_markup=keyboard)

            elif launge == "en":
                message = "No active checks"
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Menu 💫", callback_data=f'back_menu_st_{launge}')],
                    [InlineKeyboardButton(text="Back🔙", callback_data=f'balance_user_{launge}')]
                ])
                await bot.send_message(chat_id=user_id, text=message, reply_markup=keyboard)

            elif launge == "pl":
                message = "Brak aktywnych kontroli"
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Menu 💫", callback_data=f'back_menu_st_{launge}')],
                    [InlineKeyboardButton(text="Z powrotem 🔙", callback_data=f'balance_user_{launge}')]
                ])
                await bot.send_message(chat_id=user_id, text=message, reply_markup=keyboard)

            await bot.delete_message(call.message.chat.id, call.message.message_id)

        else:
            key_city = InlineKeyboardMarkup(inline_keyboard=[])

            for i in range(0, len(results), 2):
                row = []
                if i < len(results) - 1:
                    row.append(
                        InlineKeyboardButton(text=f"ID # : {results[i][0]}",
                                             callback_data=f'_check_act_{results[i][0]}_{launge}'))
                    row.append(
                        InlineKeyboardButton(text=f"ID # : {results[i + 1][0]}",
                                             callback_data=f'_check_act_{results[i + 1][0]}_{launge}'))
                else:
                    row.append(
                        InlineKeyboardButton(text=f"ID # : {results[i][0]}",
                                             callback_data=f'_check_act_{results[i][0]}_{launge}'))
                key_city.inline_keyboard.append(row)
            key_city.inline_keyboard.append([
                InlineKeyboardButton(text="Назад", callback_data=f'balance_user_{launge}')
            ])
            if launge == "ru":
                await bot.send_message(chat_id=user_id, text='Активные чеки 🧾', reply_markup=key_city)

            elif launge == "ua":
                await bot.send_message(chat_id=user_id, text='Активні чеки 🧾', reply_markup=key_city)
            elif launge == "en":
                await bot.send_message(chat_id=user_id, text='Active checks 🧾', reply_markup=key_city)
            elif launge == "pl":
                await bot.send_message(chat_id=user_id, text='Активные чеки 🧾', reply_markup=key_city)

            await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass


async def check_act_end(call: CallbackQuery, bot: Bot):
    try:
        number_check = call.data.split('_')[3]
        launge = call.data.split('_')[4]
        user_id = call.message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cheker_conf WHERE external_id = ? AND number_check = ?;", (user_id, number_check))
        results = cursor.fetchall()
        conn.close()
        message = ""
        photo = None
        for result in results:
            message += f"ID: {result[0]}\n"
            message += f"#Чека: {result[1]}\n"
            message += f"ID user: {result[2]}\n"
            message += f"Username: @{result[3]}\n"
            message += f"Цена: {result[4]}\n"
            photo = result[5]
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Меню 💫", callback_data=f'back_menu_st_{launge}')],
            [InlineKeyboardButton(text="Назад 🔙", callback_data=f'_active_check_{launge}')]
        ])
        await bot.send_photo(user_id, photo=photo, caption=message, reply_markup=keyboard)
        await bot.delete_message(user_id, call.message.message_id)
    except Exception as e:
        print(e)


async def blik(call: CallbackQuery, bot: Bot):
    try:
        launge = call.data.split('_')[1]
        if launge == "ru":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="BLIK по Номеру 📲", callback_data=f'blik_number_{launge}'),
                    InlineKeyboardButton(text="BLIK Wplata 🏦", callback_data=f'blik_wplata_{launge}')
                ],
                [
                    InlineKeyboardButton(text="Меню 💫", callback_data=f'back_menu_st_{launge}'),
                    InlineKeyboardButton(text="Назад 🔙", callback_data=f'balance_user_{launge}')
                ]
            ])
            await bot.send_message(call.message.chat.id, "BLIK 📲", reply_markup=keyboard)

        elif launge == "ua":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="BLIK за номером 📲", callback_data=f'blik_number_{launge}'),
                    InlineKeyboardButton(text="BLIK Wplata 🏦", callback_data=f'blik_wplata_{launge}')
                ],
                [
                    InlineKeyboardButton(text="Меню 💫", callback_data=f'back_menu_st_{launge}'),
                    InlineKeyboardButton(text="Назад 🔙", callback_data=f'balance_user_{launge}')
                ]
            ])
            await bot.send_message(call.message.chat.id, "BLIK 📲", reply_markup=keyboard)
        elif launge == "en":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="BLIK by Number 📲", callback_data=f'blik_number_{launge}'),
                    InlineKeyboardButton(text="BLIK Wplata 🏦", callback_data=f'blik_wplata_{launge}')
                ],
                [
                    InlineKeyboardButton(text="Menu 💫", callback_data=f'back_menu_st_{launge}'),
                    InlineKeyboardButton(text="Back 🔙", callback_data=f'balance_user_{launge}')
                ]
            ])
            await bot.send_message(call.message.chat.id, "BLIK 📲", reply_markup=keyboard)
        elif launge == "pl":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="BLIK według numeru📲", callback_data=f'blik_number_{launge}'),
                    InlineKeyboardButton(text="BLIK Wplata 🏦", callback_data=f'blik_wplata_{launge}')
                ],
                [
                    InlineKeyboardButton(text="Menu 💫", callback_data=f'back_menu_st_{launge}'),
                    InlineKeyboardButton(text="Z powrotem 🔙", callback_data=f'balance_user_{launge}')
                ]
            ])
            await bot.send_message(call.message.chat.id, "BLIK 📲", reply_markup=keyboard)

        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass


async def mess_del(call: CallbackQuery, bot: Bot):
    await bot.delete_message(call.message.chat.id, call.message.message_id)


async def history_buy_end(call: CallbackQuery, bot: Bot):
    try:
        id_value = call.data.split('_')[3]
        launge = call.data.split('_')[5]
        print(launge)
        print(id_value)
        print("dasda")

        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM active_clad WHERE id = ?", (id_value,))
        data = cursor.fetchone()
        conn.close()

        if data:
            id_value, external_id, name_city, name_area, name_item, name_gram, price_item, latitude, longtitude, photo_clad = data
            if launge == "ru":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Локация 📍",
                                             callback_data=f'_loc_clad_{latitude}_{longtitude}_{launge}')
                    ],
                    [
                        InlineKeyboardButton(text="Комментировать 📨",
                                             callback_data=f'comment_{launge}_{name_item}_{name_gram}'),
                        InlineKeyboardButton(text="Диспут ✍️", callback_data=f'dispute_{launge}_{id_value}')
                    ],
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'history_buy_{launge}'),
                        InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')
                    ]
                ])

                await bot.send_photo(call.message.chat.id, photo=photo_clad, caption=f"Город: {name_city}\n"
                                                                                     f"Район: {name_area}\n"
                                                                                     f"Товар: {name_item}\n"
                                                                                     f"Граммовка: {name_gram}\n"
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
                        InlineKeyboardButton(text="Коментувати 📨",
                                             callback_data=f'comment_{launge}_{name_item}_{name_gram}'),
                        InlineKeyboardButton(text="Диспут ✍️", callback_data=f'dispute_{launge}_{id_value}')
                    ],
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'history_buy_{launge}'),
                        InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')
                    ]
                ])

                await bot.send_photo(call.message.chat.id, photo_clad, caption=f"Місто: {name_city}\n"
                                                                               f"Район: {name_area}\n"
                                                                               f"Товар: {name_item}\n"
                                                                               f"Грамування: {name_gram}\n"
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
                        InlineKeyboardButton(text="Сomment 📨",
                                             callback_data=f'comment_{launge}_{name_item}_{name_gram}'),
                        InlineKeyboardButton(text="Dispute ✍️", callback_data=f'dispute_{launge}_{id_value}')
                    ],
                    [
                        InlineKeyboardButton(text="Back 🔙", callback_data=f'history_buy_{launge}'),
                        InlineKeyboardButton(text="Menu 💫", callback_data='back_menu_st_')
                    ]
                ])

                await bot.send_photo(call.message.chat.id, photo_clad, caption=f"City: {name_city}\n"
                                                                               f"Area: {name_area}\n"
                                                                               f"Product: {name_item}\n"
                                                                               f"Gram: {name_gram}\n"
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
                        InlineKeyboardButton(text="Komentarz 📨",
                                             callback_data=f'comment_{launge}_{name_item}_{name_gram}'),
                        InlineKeyboardButton(text="Spór ✍️", callback_data=f'dispute_{launge}_{id_value}')
                    ],
                    [
                        InlineKeyboardButton(text="Z powrotem 🔙", callback_data=f'history_buy_{launge}'),
                        InlineKeyboardButton(text="Menu 💫", callback_data='back_menu_st_')
                    ]
                ])

                await bot.send_photo(call.message.chat.id, photo_clad, caption=f"Miasto: {name_city}\n"
                                                                               f"Obszar: {name_area}\n"
                                                                               f"Produkt: {name_item}\n"
                                                                               f"Gram: {name_gram}\n"
                                                                               f"Cena: {price_item}\n"
                                                                               f"Szerokość geograficzna: {latitude}\n"
                                                                               f"Długość geograficzna: {longtitude}",
                                     reply_markup=keyboard)

            await bot.delete_message(call.message.chat.id, call.message.message_id)
        else:
            if launge == "ru":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'history_buy_{launge}')
                    ],
                    [
                        InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')
                    ]
                ])
                await bot.send_message(call.message.chat.id, "Нет данных о покупке:", reply_markup=keyboard)

            elif launge == "ua":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'history_buy_{launge}')
                    ],
                    [
                        InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')
                    ]
                ])
                await bot.send_message(call.message.chat.id, "Немає даних про купівлю:", reply_markup=keyboard)

            elif launge == "en":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Back 🔙", callback_data=f'history_buy_{launge}')
                    ],
                    [
                        InlineKeyboardButton(text="Menu 💫", callback_data='back_menu_st_')
                    ]
                ])
                await bot.send_message(call.message.chat.id, "No purchase data:", reply_markup=keyboard)

            elif launge == "pl":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Z powrotem 🔙", callback_data=f'history_buy_{launge}')
                    ],
                    [
                        InlineKeyboardButton(text="Menu 💫", callback_data='back_menu_st_')
                    ]
                ])
                await bot.send_message(call.message.chat.id, "Brak danych zakupu:", reply_markup=keyboard)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass


async def dispute(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        launge = call.data.split('_')[1]
        id_value = call.data.split('_')[2]

        await state.update_data(launge=launge)
        await state.update_data(id=id_value)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Назад 🔙", callback_data=f'history_buy_{launge}')],
        ])
        await bot.send_message(call.message.chat.id, "Опишите вашу жалобу:", reply_markup=keyboard)
        await state.set_state(Dispute.dispute_text)

        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass


async def dispute_mid(message: Message, bot: Bot, state: FSMContext):
    try:
        context_data = await state.get_data()
        launge = context_data.get('launge')

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Назад 🔙", callback_data=f'dispute_{launge}_{message.text}')],
        ])
        await state.update_data(dispute_text=message.text)
        await state.set_state(Dispute.dispute_photo)

        await bot.delete_message(message.chat.id, message.message_id - 1)
        await bot.send_message(message.chat.id, "Отправьте фотографию где  вашу жалобу: ", reply_markup=keyboard)
        await bot.delete_message(message.chat.id, message.message_id)
    except:
        pass


async def dispute_end(message: Message, bot: Bot, state: FSMContext):
    try:
        await state.update_data(dispute_photo=message.photo[-1].file_id)
        context_data = await state.get_data()

        dispute_text = context_data.get('dispute_text')
        dispute_photo = context_data.get('dispute_photo')

        id_value = context_data.get('id')
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')
            ]
        ])
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM active_clad WHERE id = ?", (id_value,))
        data = cursor.fetchone()
        conn.close()

        if data:
            id_value, external_id, name_city, name_area, name_item, name_gram, price_item, latitude, longtitude, photo_clad = data

            group_id = -1002140211473

            chat_link = f"https://t.me/{message.from_user.username}"
            button = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Начать чат", url=chat_link)
                ]
            ])
            await bot.send_photo(group_id, photo=photo_clad,
                                 caption=f"Товар: {name_item}\n"
                                         f"Город: {name_city}\n"
                                         f"Район: {name_area}\n"
                                         f"Цена: {price_item}\n"
                                         f"Граммы: {name_gram}\n"
                                         f"Жалоба снизу")

            await bot.send_photo(group_id, photo=dispute_photo,
                                 caption=f"Жалоба: {dispute_text}\n"
                                         f"Отправил: {message.from_user.full_name}\n"
                                         f"Никнейм: {message.from_user.username}\n"
                                         f"Id пользователя: {message.from_user.id}\n", reply_markup=button)

            await bot.delete_message(message.chat.id, message.message_id - 1)

            await bot.send_message(message.chat.id, "Ваша жалоба успешно отправлена.\n"
                                                    "Ожидайте обратную связь.",
                                   reply_markup=keyboard)
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM active_clad WHERE id = ?", (id_value,))
            conn.commit()
            conn.close()
            await bot.delete_message(message.chat.id, message.message_id)
        else:
            await bot.delete_message(message.chat.id, message.message_id - 1)
            await bot.send_message(message.chat.id, "Невозможно найти клад обратитесь к администрации бота.",
                                   reply_markup=keyboard)
            await bot.delete_message(message.chat.id, message.message_id)
    except:
        pass


async def comment(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        launge = call.data.split('_')[1]
        item = call.data.split('_')[2]
        gram = call.data.split('_')[3]

        await state.set_state(Comment.comment)

        await state.update_data(launge=launge)
        await state.update_data(item=item)
        await state.update_data(gram=gram)

        await bot.send_message(call.message.chat.id, f"Ваш комментарий к товару {item}:")
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass


async def comment_star(message: Message, bot: Bot, state: FSMContext):
    try:
        context_data = await state.get_data()
        comment_text = message.text
        await bot.delete_message(message.chat.id, message.message_id - 1)

        launge = context_data.get('launge')
        item = context_data.get('item')
        gram = context_data.get('gram')
        one_star = "⭐"
        two_star = "⭐⭐"
        three_star = "⭐⭐⭐"
        four_star = "⭐⭐⭐⭐"
        five_star = "⭐⭐⭐⭐⭐"
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=one_star,
                                     callback_data=f'endcomment_{launge}_{item}_{gram}_{one_star}_{comment_text}'),
            ],
            [
                InlineKeyboardButton(text=two_star,
                                     callback_data=f'endcomment_{launge}_{item}_{gram}_{two_star}_{comment_text}'),
            ],
            [
                InlineKeyboardButton(text=three_star,
                                     callback_data=f'endcomment_{launge}_{item}_{gram}_{three_star}_{comment_text}'),
            ],
            [
                InlineKeyboardButton(text=four_star,
                                     callback_data=f'endcomment_{launge}_{item}_{gram}_{four_star}_{comment_text}'),
            ],
            [
                InlineKeyboardButton(text=five_star,
                                     callback_data=f'endcomment_{launge}_{item}_{gram}_{five_star}_{comment_text}'),
            ]
        ])
        await bot.send_message(message.chat.id, f"Выберите оценку к товару {item}:", reply_markup=keyboard)
        await bot.delete_message(message.chat.id, message.message_id)
    except:
        pass


async def comment_end(call: CallbackQuery, bot: Bot):
    try:
        user_id = call.message.chat.id
        launge = call.data.split('_')[1]
        item = call.data.split('_')[2]
        gram = call.data.split('_')[3]
        star = call.data.split('_')[4]
        comment_text = call.data.split('_')[5]

        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO comment (comment_text, star, user_id, item, gram) VALUES (?, ?, ?, ?, ?)",
                       (comment_text, star, user_id, item, gram))
        conn.commit()
        conn.close()
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Menu 💫", callback_data='back_menu_st_')
            ]
        ])

        await bot.send_message(call.message.chat.id, f"Ваш комментарий к товару {item}:{comment_text}\n\n"
                                                     f"Ваша оценка: {star}\n\n"
                                                     f"Спасибо большое за комментарий!", reply_markup=keyboard)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass


async def location_clad(call: CallbackQuery, bot: Bot):
    try:
        latitude = call.data.split('_')[3]
        longtitude = call.data.split('_')[4]
        launge = call.data.split('_')[5]
        if launge == "ru":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="История покупок 🗂", callback_data=f'history_buy_{launge}')
                ],
                [
                    InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')
                ]
            ])
            if '.' in latitude or '.' in longtitude:
                print("GEY")
                latitudes = float(latitude)
                longitudes = float(longtitude)
                await bot.send_location(call.message.chat.id, latitude=latitudes, longitude=longitudes,

                                        reply_markup=keyboard)
                await bot.delete_message(call.message.chat.id, call.message.message_id)
            else:
                print("bi")

                latitudes = float(latitude.replace(',', '.'))
                longitudes = float(longtitude.replace(',', '.'))
                print(latitude, longtitude)

                await bot.send_location(call.message.chat.id, latitude=latitudes, longitude=longitudes,

                                        reply_markup=keyboard)
                await bot.delete_message(call.message.chat.id, call.message.message_id)

        elif launge == "ua":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(texagt="Історія покупок 🗂", callback_data=f'history_buy_{launge}')
                ],
                [
                    InlineKeyboardButton(text="Меню 💫", callback_data=f'back_menu_st_{launge}')
                ]
            ])
            if '.' in latitude or '.' in longtitude:
                latitudes = float(latitude)
                longitudes = float(longtitude)
                await bot.send_location(call.message.chat.id, latitude=latitudes, longitude=longitudes,

                                        reply_markup=keyboard)
                await bot.delete_message(call.message.chat.id, call.message.message_id)
            else:
                latitudes = float(latitude.replace(',', '.'))
                longitudes = float(longtitude.replace(',', '.'))
                print(latitude, longtitude)

                await bot.send_location(call.message.chat.id, latitude=latitudes, longitude=longitudes,

                                        reply_markup=keyboard)
                await bot.delete_message(call.message.chat.id, call.message.message_id)

        elif launge == "en":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(texagt="Purchase history 🗂", callback_data=f'history_buy_{launge}')
                ],
                [
                    InlineKeyboardButton(text="Menu 💫", callback_data='back_menu_st_')
                ]
            ])
            if '.' in latitude or '.' in longtitude:
                latitudes = float(latitude)
                longitudes = float(longtitude)
                await bot.send_location(call.message.chat.id, latitude=latitudes, longitude=longitudes,

                                        reply_markup=keyboard)
                await bot.delete_message(call.message.chat.id, call.message.message_id)
            else:
                latitudes = float(latitude.replace(',', '.'))
                longitudes = float(longtitude.replace(',', '.'))
                print(latitude, longtitude)

                await bot.send_location(call.message.chat.id, latitude=latitudes, longitude=longitudes,

                                        reply_markup=keyboard)
            await bot.delete_message(call.message.chat.id, call.message.message_id)

        elif launge == "pl":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(texagt="Historia zakupów 🗂", callback_data=f'history_buy_{launge}')
                ],
                [
                    InlineKeyboardButton(text="Menu 💫", callback_data='back_menu_st_')
                ]
            ])
            if '.' in latitude or '.' in longtitude:
                latitudes = float(latitude)
                longitudes = float(longtitude)
                await bot.send_location(call.message.chat.id, latitude=latitudes, longitude=longitudes,

                                        reply_markup=keyboard)
                await bot.delete_message(call.message.chat.id, call.message.message_id)
            else:
                latitudes = float(latitude.replace(',', '.'))
                longitudes = float(longtitude.replace(',', '.'))
                print(latitude, longtitude)

                await bot.send_location(call.message.chat.id, latitude=latitudes, longitude=longitudes,

                                        reply_markup=keyboard)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
