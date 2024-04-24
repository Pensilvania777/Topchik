from aiogram import Bot
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
import sqlite3

async def chek_reff(bot: Bot, message: Message):
    try:

        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()

        # Извлечение записей из таблицы refferrss
        cursor.execute("SELECT user_id, reffer_id, col_sale, reff_acative FROM refferrss")
        refferr_ids = cursor.fetchall()
        print(refferr_ids)

        for reffer_id in refferr_ids:
            user_id = reffer_id[0]
            reffer = reffer_id[1]
            col_sale = reffer_id[2]
            reff_active = reffer_id[3]

            cursor.execute("SELECT balance FROM users_shop WHERE external_id=?", (str(reffer),))
            user_data = cursor.fetchone()
            print(user_data)
            if user_data:
                balance = user_data[0]
                print(balance)
                if balance >= 100 and reff_active == 0:
                    coll_sale = col_sale + 1
                    ref_active = reff_active + 1
                    conn = sqlite3.connect('shop.db')
                    cursor = conn.cursor()

                    cursor.execute(
                        "UPDATE refferrss SET reffer_id = ?, col_sale = ?, reff_acative = ? WHERE user_id = ?",
                        (reffer, coll_sale, ref_active, user_id))

                    conn.commit()
                    conn.close()
        conn.close()
    except Exception as e:
        print(e)