from aiogram import Bot
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
import sqlite3
import aiohttp
from aiocryptopay import AioCryptoPay, Networks
from utils.state import Asset_summ
from aiogram.fsm.context import FSMContext




API_TOKEN = '142892:AADgzNpCof3FEodM71u3T7Gjrw3BSOKBat5'

crypto_assets = ['USDT', 'USDC', 'BTC', 'BNB', 'TRX', 'TON', 'ETH', 'LTC']


async def get_conversion_amount(summ, money):
    async with aiohttp.ClientSession() as session:
        crypto = AioCryptoPay(token=API_TOKEN, network=Networks.MAIN_NET)
        money = str(money.upper())
        summ_float = float(summ)
        rates = await crypto.get_exchange_rates()
        print(rates)
        print("DASDSAFAGDGAGFDSADASD",summ, money)
        amount = await crypto.get_amount_by_fiat(summ=summ_float, asset=money, target='PLN')
    return amount


async def cryptos(call: CallbackQuery, bot: Bot):
    try:
        launge = call.data.split('_')[1]
        user_id = call.message.chat.id

        button_rows = [crypto_assets[i:i + 3] for i in range(0, len(crypto_assets), 3)]

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=asset, callback_data=f'_summ_{asset.lower()}_{launge}') for asset in row] for row
            in button_rows
        ])
        if launge == "ru":
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT text_crypto, photo_crypto FROM oform_ru WHERE id = ?''', (1,))

            result = cursor.fetchone()
            text_menu = ""
            photo_menu = ""
            if result:
                text_menu, photo_menu = result
            conn.close()

            await bot.send_photo(call.message.chat.id, photo_menu,
                                 caption="Выберите криптовалюту, которой хотите оплатить:", reply_markup= keyboard)
        elif launge == "ua":
            await bot.send_message(user_id, "Виберіть криптовалюту, яку хочете сплатити:", reply_markup=keyboard)
        elif launge == "en":
            await bot.send_message(user_id, "Select the cryptocurrency you want to pay with:", reply_markup=keyboard)
        elif launge == "pl":
            await bot.send_message(user_id, "Wybierz kryptowalutę, którą chcesz zapłacić:", reply_markup=keyboard)

        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass

async def process_summ(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id
        asset = call.data.split('_')[2]
        launge = call.data.split('_')[3]

        await state.update_data(asset=asset)
        await state.update_data(launge=launge)
        if launge == "ru":
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT text_crypto, photo_crypto FROM oform_ru WHERE id = ?''', (1,))

            result = cursor.fetchone()
            text_menu = ""
            photo_menu = ""
            if result:
                text_menu, photo_menu = result
            conn.close()

            await bot.send_photo(call.message.chat.id, photo_menu,
                                 caption=f"Введите количество Zloty на которую вы хотите пополнить {asset}:")
        elif launge == "en":
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT text_crypto, photo_crypto FROM oform_en WHERE id = ?''', (1,))

            result = cursor.fetchone()
            text_menu = ""
            photo_menu = ""
            if result:
                text_menu, photo_menu = result
            conn.close()

            await bot.send_photo(call.message.chat.id, photo_menu,
                                 caption=f"Enter the amount Zloty with which you want to top up {asset}:")
        await state.set_state(Asset_summ.summ_asset)
        await bot.delete_message(user_id, call.message.message_id)
    except:
        pass


async def process_amount(message: Message, bot: Bot, state: FSMContext):
    context_data = await state.get_data()
    asset = context_data.get('asset')
    launge = context_data.get('launge')

    try:
        await bot.delete_message(message.chat.id, message.message_id)
        sum = float(message.text)
        print(sum)

        if launge == "ru":
            response_text = f"Вы хотите пополнить {asset} на {sum} Zlot"
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Отменить", callback_data=f'balance_user_{launge}')
                ],
                [
                    InlineKeyboardButton(text="Подтвердить", callback_data=f'_crypter_{sum}_{asset}_{launge}')
                ]
            ])
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT text_crypto, photo_crypto FROM oform_ru WHERE id = ?''', (1,))

            result = cursor.fetchone()
            text_menu = ""
            photo_menu = ""
            if result:
                text_menu, photo_menu = result
            conn.close()

            await bot.send_photo(message.chat.id, photo_menu,
                                 caption=response_text,
                                 reply_markup=keyboard)

            await bot.delete_message(message.chat.id, message.message_id - 1)


        elif launge == "en":
            response_text = f"Do you want to top up {asset} with {sum} Zlot ? "
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Cancel", callback_data=f'balance_user_{launge}')
                ],
                [
                    InlineKeyboardButton(text="Confirm", callback_data=f'_crypter_{sum}_{asset}_{launge}')
                ]
            ])
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT text_crypto, photo_crypto FROM oform_en WHERE id = ?''', (1,))

            result = cursor.fetchone()
            text_menu = ""
            photo_menu = ""
            if result:
                text_menu, photo_menu = result
            conn.close()

            await bot.send_photo(message.chat.id, photo_menu,
                                 caption=response_text,
                                 reply_markup=keyboard)

            await bot.delete_message(message.chat.id, message.message_id - 1)

    except ValueError:
        await bot.send_message(message.chat.id, "Некорректная сумма. Пожалуйста, введите число.")


async def process_crypto_payment(call: CallbackQuery, bot: Bot):
    try:
        user_id = call.message.chat.id
        summ = call.data.split('_')[2]
        asset = call.data.split('_')[3]
        launge = call.data.split('_')[4]

        # Получаем конвертированное значение суммы
        amount = await get_conversion_amount(summ, asset)

        if amount is not None:
            crypto = AioCryptoPay(token=API_TOKEN, network=Networks.MAIN_NET)
            print(amount)
            invoice = await crypto.create_invoice(asset=asset, amount=amount)

            payment_link = invoice.bot_invoice_url
            invoices = await crypto.get_invoices(invoice_ids=[invoice.invoice_id])
            invoice_id = invoice.invoice_id
        else:
            print("Conversion failed.")

        if launge == "ru":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Оплачено ✅",
                                         callback_data=f'_pay_active_{invoices[0].status}_{invoice_id}_{summ}_{asset}_{launge}')
                ],
                [
                    InlineKeyboardButton(text="Отменить", callback_data=f'balance_user_{launge}')
                ]
            ])
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT text_crypto, photo_crypto FROM oform_ru WHERE id = ?''', (1,))

            result = cursor.fetchone()
            text_menu = ""
            photo_menu = ""
            if result:
                text_menu, photo_menu = result
            conn.close()

            await bot.send_photo(user_id, photo_menu, caption=f"Пожалуйста, оплатите{asset} на сумму {summ} Zlot по ссылке:\n{payment_link}", reply_markup=keyboard)


        elif launge == "en":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Paid ✅",
                                         callback_data=f'_pay_active_{invoices[0].status}_{invoice_id}_{sum}_{asset}_{launge}')
                ],
                [
                    InlineKeyboardButton(text="Cancel", callback_data=f'balance_user_{launge}')
                ]
            ])
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT text_crypto, photo_crypto FROM oform_en WHERE id = ?''', (1,))

            result = cursor.fetchone()
            text_menu = ""
            photo_menu = ""
            if result:
                text_menu, photo_menu = result
            conn.close()

            await bot.send_photo(user_id, photo_menu,
                                 caption=f"Please pay {asset} in the amount of {summ} Zlot using the link:\n{payment_link}",
                                 reply_markup=keyboard)



        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(repr(e))


async def active_pay(call: CallbackQuery, bot: Bot):
    try:
        invoice = call.data.split('_')[3]
        invoice_id = call.data.split('_')[4]
        summ = call.data.split('_')[5]
        asset = call.data.split('_')[6]
        launge = call.data.split('_')[7]

        print(invoice_id)

        print(invoice)
        user_id = call.message.chat.id

        if invoice == 'paid':
            print("Инвойс оплачен!")
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE users_shop SET balance = balance + ? WHERE external_id = ?", (summ, user_id))
            conn.commit()
            conn.close()
            if launge == "ru":
                conn = sqlite3.connect('shop.db')
                cursor = conn.cursor()
                cursor.execute('''SELECT text_crypto, photo_crypto FROM oform_ru WHERE id = ?''', (1,))

                result = cursor.fetchone()
                text_menu = ""
                photo_menu = ""
                if result:
                    text_menu, photo_menu = result
                conn.close()
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Меню", callback_data='back_menu_st_')
                    ]
                ])
                await bot.send_photo(user_id, photo_menu, caption=f"Платеж оплачен.\n"
                                                f"Баланс обновлен.", reply_markup=keyboard)
            elif launge == "ua":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Меню", callback_data='back_menu_st_')
                    ]
                ])
                await bot.send_message(user_id, f"Платіж сплачено.\n"
                                                f"Баланс оновлено.", reply_markup=keyboard)

            elif launge == "en":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Menu", callback_data='back_menu_st_')
                    ]
                ])
                await bot.send_message(user_id, f"Payment paid.\n"
                                                f"Balance updated.", reply_markup=keyboard)

            elif launge == "pl":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Menu", callback_data='back_menu_st_')
                    ]
                ])
                await bot.send_message(user_id, f"Płatność opłacona.\n"
                                                f"Saldo zaktualizowane.", reply_markup=keyboard)



        else:
            if launge == "ru":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Назад", callback_data=f'_crypter_{summ}_{asset}_{launge}')
                    ],
                    [
                        InlineKeyboardButton(text="Меню", callback_data='back_menu_st')
                    ]
                ])
                conn = sqlite3.connect('shop.db')
                cursor = conn.cursor()
                cursor.execute('''SELECT text_crypto, photo_crypto FROM oform_ru WHERE id = ?''', (1,))

                result = cursor.fetchone()
                text_menu = ""
                photo_menu = ""
                if result:
                    text_menu, photo_menu = result
                conn.close()

                await bot.send_photo(user_id, photo_menu, caption=f"Платеж не оплачен.", reply_markup=keyboard)

            elif launge == "ua":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Назад", callback_data=f'_crypter_{summ}_{asset}_{launge}')
                    ],
                    [
                        InlineKeyboardButton(text="Меню", callback_data='back_menu_st')
                    ]
                ])

                await bot.send_message(user_id, f"Платіж не сплачено.", reply_markup=keyboard)

            elif launge == "en":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Back", callback_data=f'_crypter_{summ}_{asset}_{launge}')
                    ],
                    [
                        InlineKeyboardButton(text="Menu", callback_data='back_menu_st')
                    ]
                ])

                await bot.send_message(user_id, f"Payment not paid.", reply_markup=keyboard)
            elif launge == "pl":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Z powrotem", callback_data=f'_crypter_{summ}_{asset}_{launge}')
                    ],
                    [
                        InlineKeyboardButton(text="Menu", callback_data='back_menu_st')
                    ]
                ])
                await bot.send_message(user_id, f"Płatność nie została uiszczona.", reply_markup=keyboard)

            await bot.delete_message(call.message.chat.id, call.message.message_id)
            print("Инвойс не оплачен.")
    except:
        pass