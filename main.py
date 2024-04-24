import asyncio
import logging
import sys
import sqlite3
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ContentType)

from aiogram.filters import CommandStart, Command
from admin_handlers.admin_oform import (ofor_menu, ofor_menu_add_start, ofor_menu_add, ofor_laguange_add,
                                        ofor_balance_add_start, ofor_blik_add_start)
import config
from admin_handlers.admin_oform_en import (add_oform_rules_end_en, add_oform_crypto_end_en,add_oform_profile_end_en,
                                           add_oform_photo_rules_en, add_oform_photo_area_en, add_oform_area_end_en,
                                           add_oform_banc_end_en,add_oform_city_end_en, add_oform_photo_banc_en,
                                           add_oform_item_end_en, add_oform_menu_end_en, add_oform_photo_item_en,
                                           add_oform_reff_end_en, add_oform_photo_reff_en, add_oform_photo_city_en,
                                           add_oform_photo_menu_en, add_oform_photo_actcheck_en, add_oform_actcheck_end_en,
                                           add_oform_end_en_blik, add_oform_instruction_end_en, add_oform_izbpokup_end_en,
                                           add_oform_language_end_en, add_oform_photo_language_en, add_oform_photo_blikwplata_en
                                           , add_oform_photo_crypto_en, add_oform_photo_instuction_en, add_oform_photo_izbpokup_en
                                           , add_oform_photo_profile_en, oform_start_area_en, oform_start_actcheck_en,
                                           oform_start_banc_en, oform_start_city_en, oform_start_item_en, oform_start_menu_en,
                                           oform_start_reff_en, oform_start_rules_en, oform_start_crypto_en, oform_start_izbpokup_en,
                                           oform_start_language_en, oform_start_blikwplata_en, oform_start_instuction_en)
from admin_handlers.admin_oform_ru import (oform_start_rules,oform_start_instuction, oform_start_area, oform_start_city,
                                           oform_start_menu, oform_start_language, add_oform_rules_end,add_oform_menu_end,
                                           add_oform_area_end, add_oform_city_end, add_oform_language_end, add_oform_photo_area
                                           , add_oform_photo_city, add_oform_photo_menu, add_oform_photo_language,
                                           add_oform_photo_rules, add_oform_photo_instuction, oform_start_item, add_oform_item_end,
                                           add_oform_photo_item,add_oform_instruction_end, add_oform_profile_end,
                                           add_oform_photo_profile, add_oform_crypto_end, add_oform_actcheck_end,
                                           add_oform_blickwplata_end, add_oform_photo_crypto, add_oform_photo_actcheck,
                                           add_oform_photo_blikwplata, oform_start_crypto, oform_start_actcheck,
                                           oform_start_blikwplata, add_oform_number_phone, add_oform_iban, add_oform_blick_end
                                           , add_oform_name_blik, oform_start_izbpokup, oform_start_banc , oform_start_reff
                                           , add_oform_photo_banc, add_oform_photo_izbpokup, add_oform_izbpokup_end,
                                           add_oform_reff_end, add_oform_banc_end, add_oform_photo_reff)
from handlers.pay_blick import blik_number
from handlers.callback import( buy_insert, return_start, my_acc, history_buy, balance_user, active_check, blik, mess_del,
                                 comment_run, comment_star, check_act_end, history_buy_end, dispute, dispute_mid, dispute_end,
                                 comment_end, process_callback,  reffer_system, language, comment ,language_end,location_clad,
                               copy_text)
from handlers.pay_crypto import cryptos,process_summ,active_pay,process_amount, crypto_assets, process_crypto_payment

from handlers.buy_clad import buy_clad, buy_area,buy_item, buy_item_end , buy_end_ars , buy_gram

from handlers.admin_callback import ( delete_blick_end, confirm_blik_end, confirm_blik_mid,
                                     confirm_blik)
from handlers.cladman_menu import (add_clad_cladman,add_clad_grams_cladman, add_clad_photo_cladman, add_clad_end_cladman,
                                   add_clad_lat_cladman, add_clad_area_cladman, add_clad_gram_cladman, add_clad_item_cladman,
                                   add_clad_long_cladman, cladman_menu)
from handlers.basic import get_start, start_reff, language_start_set, generate_animal_captcha, on_button_pressed
from admin_handlers.admin_menu import admin_handler, admin_return_menu
from admin_handlers.admin_analis import (admin_analis_day, admin_analis_day_mid, admin_analis_day_end, admin_analis_mont_st,
                                         admin_analis, admin_analis_mont, admin_analis_mid, admin_analis_week)
from admin_handlers.admin_send import (admin_message_true, admin_message_photo, admin_message_end)
from admin_handlers.admin_city import (admin_city_menu, add_city, add_city_end, del_city, del_city_end, show_city)
from admin_handlers.admin_set import (admin_set_add_name,
                                     admin_set_add_end, admin_set_add_external, admin_show_set,
                                     admin_set_menu, del_admin_end, del_admin_set)
from admin_handlers.admin_area import (admin_area_menu, add_area, add_area_end, add_area_central
                                        , del_area, del_area_end, show_area)
from admin_handlers.admin_item import (add_item, add_item_end, add_item_center, add_item_photo, add_item_price,
                                     admin_item_menu, del_item, del_item_end, show_item, show_end)
from admin_handlers.admin_gram import (admin_gram_menu, add_gram, add_gram_end, del_gram_end, show_gram, del_gram)
from admin_handlers.admin_balance import (admin_balance_menu, add_balance_set, add_balance_ex_end, add_balance_end, del_balance_end,
                                     del_balance_set, show_balance, del_balance_ex_end)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from admin_handlers.admin_clad import (add_clad_end, add_clad_photo, add_clad, add_clad_lat, add_clad_item
                                     , admin_clad_menu, add_clad_area, add_clad_gram, add_clad_grams, add_clad_long
                                     , del_clad, show_clad, del_clad_end, show_clad_item, show_clad_area, show_clad_gram,show_clad_end)
from admin_handlers.admin_cladman import (admin_cladman, admin_cladman_menu, admin_cladman_end,admin_cladman_mid,
                                         admin_show_cladman,del_cladman_end,del_cladman)
from handlers.pay_blick import (blik_number,  can_check_call,
                                buy_check_photo, buy_check_end, blik_number_end, del_check_end, end_check)
from utils.state import (Rass, City, Admin, Area, Item, Gram, Balance,
                         Balance_del, Clad, Asset_summ, Dispute, Captcha, Comment, CladMan, CladManJob, Blick_payment,
                         oform_ru, oform_en)
from aiogram import F
from handlers.pay_blik_wplata import pay_blik_wplata
from handlers.rules import rules
from handlers.instruction import instruction
from handlers.refferal import chek_reff
TOKEN = config.TOKEN

conn = sqlite3.connect('shop.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users_shop(
                           id INTEGER PRIMARY KEY,
                           name_user TEXT,
                           external_id TEXT,
                           launge_user TEXT DEFAULT 'ru',
                           balance INTEGER DEFAULT 0,
                           col_buy INTEGER DEFAULT 0,
                           open_dispute INTEGER DEFAULT 0,
                           close_dispute INTEGER DEFAULT 0
                       )''')
conn.commit()
conn.close()


conn = sqlite3.connect('shop.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS admin(
                           id INTEGER PRIMARY KEY,
                           name_admin TEXT,
                           external_admin TEXT
                       )''')
conn.commit()
conn.close()

conn = sqlite3.connect('shop.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS cladman(
                           id INTEGER PRIMARY KEY,
                           name_cladman TEXT,
                           external_cladman TEXT
                       )''')
conn.commit()
conn.close()


conn = sqlite3.connect('shop.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS city(
                           id INTEGER PRIMARY KEY,
                           name_city TEXT
                       )''')
conn.commit()
conn.close()


conn = sqlite3.connect('shop.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS grams(
                           id INTEGER PRIMARY KEY,
                           gram TEXT
                       )''')
conn.commit()
conn.close()

conn = sqlite3.connect('shop.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS area(
                           id INTEGER PRIMARY KEY,
                           name_city TEXT,
                           name_area TEXT
                       )''')
conn.commit()
conn.close()

conn = sqlite3.connect('shop.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS item(
                           id INTEGER PRIMARY KEY,
                           name_item TEXT,
                           caption_item TEXT,
                           price_item TEXT,
                           photo_item BLOB
                       )''')
conn.commit()
conn.close()

conn = sqlite3.connect('shop.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS check_def(
                           id INTEGER PRIMARY KEY,
                           number_check INTEGER DEFAULT 0,
                           external_id TEXT
                       )''')
conn.commit()
conn.close()

conn = sqlite3.connect('shop.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS cheker(
                           id INTEGER PRIMARY KEY,
                           number_check INTEGER,
                           external_id TEXT,
                           name_user TEXT,
                           price TEXT, 
                           photo_check BLOB
                       )''')
conn.commit()
conn.close()

conn = sqlite3.connect('shop.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS cheker_conf(
                           id INTEGER PRIMARY KEY,
                           number_check INTEGER,
                           external_id TEXT,
                           name_user TEXT,
                           price TEXT, 
                           photo_check BLOB
                       )''')
conn.commit()
conn.close()

conn = sqlite3.connect('shop.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS clad(
                           id INTEGER PRIMARY KEY,
                           name_city TEXT,
                           name_area TEXT,
                           name_item TEXT,
                           name_gram TEXT,
                           price_item TEXT,
                           latitude TEXT,
                           longtitude TEXT,
                           photo_clad BLOB
                       )''')
conn.commit()
conn.close()

conn = sqlite3.connect('shop.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS active_clad(
                           id INTEGER PRIMARY KEY,
                           external_id TEXT,
                           name_city TEXT,
                           name_area TEXT,
                           name_item TEXT,
                           name_gram TEXT,
                           price_item TEXT,
                           latitude TEXT,
                           longtitude TEXT,
                           photo_clad BLOB
                       )''')
conn.commit()
conn.close()

conn = sqlite3.connect('shop.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS oform_ru(
                           id INTEGER PRIMARY KEY,
                           text_menu TEXT,
                           text_city TEXT,
                           text_area TEXT,
                           text_language TEXT,
                           text_instuction TEXT,
                           text_rules TEXT,
                           text_item TEXT,
                           text_profile TEXT,
                           text_actcheck TEXT,
                           text_crypto TEXT,
                           text_blick_number TEXT,
                           text_blick_wplata TEXT,
                           text_banc TEXT,
                           text_izbpokup TEXT,
                           text_reff TEXT,
                           photo_menu BLOB,
                           photo_city BLOB,
                           photo_area BLOB,
                           photo_language BLOB,
                           photo_instruction BLOB,
                           photo_rules BLOB,
                           photo_profile BLOB,
                           photo_item BLOB,
                           photo_actcheck BLOB,
                           photo_crypto BLOB,
                           photo_blick_number BLOB,
                           photo_blick_wplata BLOB,
                           photo_banc BLOB,
                           photo_izbpokup BLOB,
                           photo_reff BLOB
                       )''')
conn.commit()
conn.close()


conn = sqlite3.connect('shop.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS oform_en(
                           id INTEGER PRIMARY KEY,
                           text_menu TEXT,
                           text_city TEXT,
                           text_area TEXT,
                           text_language TEXT,
                           text_instuction TEXT,
                           text_rules TEXT,
                           text_item TEXT,
                           text_profile TEXT,
                           text_actcheck TEXT,
                           text_crypto TEXT,
                           text_blick_number TEXT,
                           text_blick_wplata TEXT,
                           text_banc TEXT,
                           text_izbpokup TEXT,
                           text_reff TEXT,
                           photo_menu BLOB,
                           photo_city BLOB,
                           photo_area BLOB,
                           photo_language BLOB,
                           photo_instruction BLOB,
                           photo_rules BLOB,
                           photo_profile BLOB,
                           photo_item BLOB,
                           photo_actcheck BLOB,
                           photo_crypto BLOB,
                           photo_blick_number BLOB,
                           photo_blick_wplata BLOB,
                           photo_banc BLOB,
                           photo_izbpokup BLOB,
                           photo_reff BLOB
                       )''')
conn.commit()
conn.close()

conn = sqlite3.connect('shop.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS analist(
                           id INTEGER PRIMARY KEY,
                           city INTEGER,
                           item TEXT,
                           col TEXT,
                           price TEXT,
                           day TEXT,
                           mont TEXT
                       )''')
conn.commit()
conn.close()

conn = sqlite3.connect('shop.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS refferrss(
                           id INTEGER PRIMARY KEY,
                           user_id INTEGER DEFAULT 0,
                           reffer_id INTEGER,
                           col_sale INTEGER,
                           reff_acative INTEGER
                       )''')
conn.commit()
conn.close()

conn = sqlite3.connect('shop.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS comment(
                           id INTEGER PRIMARY KEY,    
                           comment_text TEXT,
                           star TEXT,
                           user_id TEXT,
                           item TEXT,
                           gram TEXT
                       )''')
conn.commit()
conn.close()

conn = sqlite3.connect('shop.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS blik(
                           id INTEGER PRIMARY KEY,    
                           text_iban TEXT,
                           text_number_phone TEXT,
                           text_nameuser TEXT
                       )''')
conn.commit()
conn.close()





logging.basicConfig(level=logging.INFO)


async def start():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(router=Router())
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(chek_reff, trigger='interval', seconds=120,
                      kwargs=({'bot': bot, 'message': Message}))
    scheduler.start()

    dp.message.register(start_reff, CommandStart())
    dp.message.register(admin_handler, Command("admin"))
    dp.message.register(cladman_menu, Command("cladman"))

    dp.callback_query.register(return_start, F.data.startswith("back_menu_st_"))
    dp.callback_query.register(on_button_pressed, F.data.startswith("check_animal_"))

    dp.callback_query.register(balance_user, F.data.startswith("balance_user_"))
    dp.callback_query.register(active_check, F.data.startswith("_active_check_"))
    dp.callback_query.register(history_buy, F.data.startswith("history_buy_"))
    dp.callback_query.register(buy_clad, F.data.startswith("buy_ins_"))
    dp.callback_query.register(my_acc, F.data.startswith("my_acc_"))
    dp.callback_query.register(blik, F.data.startswith("bliker_"))

    dp.callback_query.register(rules, F.data.startswith("faq_"))
    dp.callback_query.register(instruction, F.data.startswith("instruction_"))

    dp.callback_query.register(mess_del, F.data.startswith("mess_del"))
    dp.callback_query.register(admin_message_true, F.data.startswith("admin_message"))
    dp.message.register(admin_message_photo, Rass.rass_text)
    dp.message.register(admin_message_end, Rass.rass_photo)

    dp.callback_query.register(admin_city_menu, F.data.startswith("admin_city"))
    dp.callback_query.register(add_city, F.data.startswith("add_city"))
    dp.callback_query.register(del_city, F.data.startswith("del_city"))
    dp.callback_query.register(del_city_end, F.data.startswith("_city_del_"))
    dp.message.register(add_city_end, City.city_add)
    dp.callback_query.register(show_city, F.data.startswith("show_city"))
    dp.callback_query.register(admin_return_menu, F.data.startswith("admin_command"))

    dp.callback_query.register(admin_set_add_name, F.data.startswith("add_admin_set_"))
    dp.callback_query.register(del_admin_set, F.data.startswith("del_admin_set_"))
    dp.callback_query.register(del_admin_end, F.data.startswith("_admin_del_"))
    dp.callback_query.register(admin_show_set, F.data.startswith("show_admin_set_"))
    dp.callback_query.register(admin_set_menu, F.data.startswith("admin_setting"))
    dp.callback_query.register(pay_blik_wplata, F.data.startswith("blik_wplata_"))

    dp.message.register(admin_set_add_external, Admin.admin_name)
    dp.message.register(admin_set_add_end, Admin.admin_id)
    dp.callback_query.register(admin_area_menu, F.data.startswith("admin_area"))
    dp.callback_query.register(add_area, F.data.startswith("add_area_set_"))
    dp.callback_query.register(add_area_central, F.data.startswith("_city_area_"))
    dp.message.register(add_area_end, Area.name_area)
    dp.callback_query.register(del_area, F.data.startswith("del_area_set_"))
    dp.callback_query.register(del_area_end, F.data.startswith("/area/del/"))
    dp.callback_query.register(show_area, F.data.startswith("show_area_set_"))

    dp.callback_query.register(admin_item_menu, F.data.startswith("admin_item"))
    dp.callback_query.register(add_item, F.data.startswith("add_item_set_"))
    dp.callback_query.register(show_item, F.data.startswith("show_item_set_"))
    dp.callback_query.register(show_end, F.data.startswith("_item_show_"))
    dp.callback_query.register(del_item, F.data.startswith("del_item_set_"))
    dp.callback_query.register(del_item_end, F.data.startswith("_item_del_"))
    dp.message.register(add_item_center, Item.name_item)
    dp.message.register(add_item_price, Item.name_opis)
    dp.message.register(add_item_photo, Item.price_item)
    dp.message.register(add_item_end, Item.photo_item)

    dp.callback_query.register(admin_gram_menu, F.data.startswith("admin_gram"))
    dp.callback_query.register(add_gram, F.data.startswith("add_gram_set_"))
    dp.message.register(add_gram_end, Gram.name_gram)
    dp.callback_query.register(del_gram, F.data.startswith("del_gram_set_"))
    dp.callback_query.register(del_gram_end, F.data.startswith("_gram_del_"))
    dp.callback_query.register(show_gram, F.data.startswith("show_gram_set_"))

    dp.callback_query.register(admin_balance_menu, F.data.startswith("admin_balance"))
    dp.callback_query.register(add_balance_set, F.data.startswith("add_balance_set_"))
    dp.message.register(add_balance_end, Balance.external_id)
    dp.message.register(add_balance_ex_end, Balance.balance_summ)
    dp.message.register(del_balance_end, Balance_del.external_id_del)
    dp.message.register(del_balance_ex_end, Balance_del.balance_del)
    dp.callback_query.register(show_balance, F.data.startswith("show_balance_set_"))
    dp.callback_query.register(del_balance_set, F.data.startswith("del_balance_set_"))
    dp.callback_query.register(location_clad, F.data.startswith("_loc_clad_"))

    dp.callback_query.register(admin_clad_menu, F.data.startswith("admin_clad"))
    dp.callback_query.register(add_clad, F.data.startswith("add_clad_set_"))
    dp.callback_query.register(add_clad_area, F.data.startswith("_clad_city_"))
    dp.callback_query.register(add_clad_item, F.data.startswith("_clad_area_"))
    dp.callback_query.register(add_clad_gram, F.data.startswith("_clad_item_"))
    dp.callback_query.register(add_clad_grams, F.data.startswith("_clad_gram_"))
    dp.message.register(add_clad_lat, Clad.latit)
    dp.message.register(add_clad_long, Clad.longtit)
    dp.message.register(add_clad_photo, Clad.longdob)
    dp.message.register(add_clad_end, Clad.photo_clad)
    dp.callback_query.register(del_clad, F.data.startswith("del_clad_set_"))
    dp.message.register(del_clad_end, Clad.del_clad)
    dp.callback_query.register(show_clad, F.data.startswith("show_clad_set_"))

    dp.callback_query.register(confirm_blik, F.data.startswith("admin_check"))
    dp.callback_query.register(confirm_blik_mid, F.data.startswith("_blik_confirm_"))
    dp.callback_query.register(confirm_blik_end, F.data.startswith("blik_okey_"))
    dp.callback_query.register(delete_blick_end, F.data.startswith("blik_delete_"))



    dp.callback_query.register(buy_area, F.data.startswith("_ars_item_"))
    dp.callback_query.register(buy_item, F.data.startswith("_ars_city_"))
    dp.callback_query.register(buy_gram, F.data.startswith("_ars_area_"))

    dp.callback_query.register(buy_item_end, F.data.startswith("_ars_gram_"))
    dp.callback_query.register(buy_end_ars, F.data.startswith("_ars_end_"))

    dp.callback_query.register(history_buy_end, F.data.startswith("_view_item_"))
    dp.callback_query.register(cryptos, F.data.startswith("crypto_"))
    dp.callback_query.register(process_summ, F.data.startswith("_summ_"))
    dp.message.register(process_amount, Asset_summ.summ_asset)
    dp.callback_query.register(process_crypto_payment, F.data.startswith("_crypter_"))
    dp.callback_query.register(active_pay, F.data.startswith("_pay_active_"))

    dp.callback_query.register(admin_analis, F.data.startswith("admin_analis"))
    dp.callback_query.register(admin_analis_mid, F.data.startswith("_analis_city_"))
    dp.callback_query.register(admin_analis_mont, F.data.startswith("analis_monest_"))
    dp.callback_query.register(admin_analis_mont_st, F.data.startswith("_analis_mont_"))
    dp.callback_query.register(admin_analis_week, F.data.startswith("_analis_week_"))
    dp.callback_query.register(admin_analis_day, F.data.startswith("_analis_day_"))
    dp.callback_query.register(admin_analis_day_mid, F.data.startswith("analis_montsa"))
    dp.callback_query.register(admin_analis_day_end, F.data.startswith("day_analis_"))

    dp.callback_query.register(reffer_system, F.data.startswith("reffer_system_"))

    dp.callback_query.register(language_start_set, F.data.startswith("laungeuage_start_"))
    dp.callback_query.register(language, F.data.startswith("language"))
    dp.callback_query.register(language_end, F.data.startswith("laungeuage_set_"))

    dp.callback_query.register(comment, F.data.startswith("comment_"))
    dp.message.register(comment_star, Comment.comment)
    dp.callback_query.register(comment_end, F.data.startswith("endcomment_"))

    dp.callback_query.register(comment_run, F.data.startswith("comview_"))
    dp.callback_query.register(process_callback, F.data.startswith("prev"))
    dp.callback_query.register(process_callback, F.data.startswith("next"))

    dp.callback_query.register(dispute, F.data.startswith("dispute_"))
    dp.message.register(dispute_mid, Dispute.dispute_text)
    dp.message.register(dispute_end, Dispute.dispute_photo)

    dp.callback_query.register(generate_animal_captcha, F.data.startswith("captcha_"))

    dp.callback_query.register(admin_cladman_menu, F.data.startswith("cladman_"))

    dp.callback_query.register(admin_cladman, F.data.startswith("add_cladman"))
    dp.message.register(admin_cladman_mid, CladMan.name_cladman)
    dp.message.register(admin_cladman_end, CladMan.external_id_cladman)

    dp.callback_query.register(del_cladman, F.data.startswith("del_cladman"))
    dp.callback_query.register(del_cladman_end, F.data.startswith("_cladman_del_"))

    dp.callback_query.register(admin_show_cladman, F.data.startswith("show_cladman"))

    dp.callback_query.register(add_clad_cladman, F.data.startswith("cm_cl"))
    dp.callback_query.register(add_clad_area_cladman, F.data.startswith("_cladman_city_"))
    dp.callback_query.register(add_clad_item_cladman, F.data.startswith("_cladman_area_"))
    dp.callback_query.register(add_clad_gram_cladman, F.data.startswith("_cladman_item_"))
    dp.callback_query.register(add_clad_grams_cladman, F.data.startswith("_cladman_gram_"))
    dp.message.register(add_clad_lat_cladman, CladManJob.latit)
    dp.message.register(add_clad_long_cladman, CladManJob.longtit)
    dp.message.register(add_clad_photo_cladman, CladManJob.longdob)
    dp.message.register(blik_number_end, Blick_payment.summ_blick)
    dp.callback_query.register(blik_number, F.data.startswith("blik_number"))

    dp.callback_query.register(buy_check_photo, F.data.startswith("_buy_check_"))
    dp.callback_query.register(end_check, F.data.startswith("_end_check_"))
    dp.callback_query.register(can_check_call, F.data.startswith("_can_ch_"))
    dp.callback_query.register(del_check_end, F.data.startswith("_del_check_"))
    dp.callback_query.register(check_act_end, F.data.startswith("_check_act_"))

    dp.callback_query.register(show_clad, F.data.startswith("show_clad_set_"))
    dp.callback_query.register(show_clad_item, F.data.startswith("city_admin_show_"))
    dp.callback_query.register(show_clad_area, F.data.startswith("admin_show_item_"))
    dp.callback_query.register(show_clad_gram, F.data.startswith("gram_admin_show_"))
    dp.callback_query.register(show_clad_end, F.data.startswith("end_clad_show_"))

    dp.callback_query.register(ofor_menu, F.data.startswith("oform_"))
    dp.callback_query.register(ofor_laguange_add, F.data.startswith("admin_oform_menu_add"))
    dp.callback_query.register(ofor_menu_add_start, F.data.startswith("admin_oform_go_"))


    dp.callback_query.register(ofor_menu_add, F.data.startswith("admin_language_"))


    dp.message.register(buy_check_end, Blick_payment.check_end)

    dp.callback_query.register(add_oform_iban, F.data.startswith("admin_oform_blik_number_"))
    dp.message.register(add_oform_number_phone, oform_ru.text_iban)
    dp.message.register(add_oform_name_blik, oform_ru.text_number_phone)
    dp.message.register(add_oform_blick_end, oform_ru.text_name_poluch)

    dp.callback_query.register(ofor_balance_add_start, F.data.startswith("admin_oform_balance_"))
    dp.callback_query.register(ofor_blik_add_start, F.data.startswith("admin_oform_blik_"))

    dp.callback_query.register(oform_start_blikwplata, F.data.startswith("blik_admin_wplata_"))
    dp.message.register(add_oform_photo_blikwplata, oform_ru.text_blik_wplata)
    dp.message.register(add_oform_blickwplata_end, oform_ru.photo_blik_wplata)

    dp.message.register(add_clad_end_cladman, CladManJob.photo_clad)

    dp.callback_query.register(oform_start_menu, F.data.startswith("admin_oform_start_menu_ru_"))
    dp.message.register(add_oform_photo_menu, oform_ru.text_menu)
    dp.message.register(add_oform_menu_end, oform_ru.photo_menu)

    dp.callback_query.register(oform_start_city, F.data.startswith("admin_oform_city_ru_"))
    dp.message.register(add_oform_photo_city, oform_ru.text_city)
    dp.message.register(add_oform_city_end, oform_ru.photo_city)

    dp.callback_query.register(oform_start_area, F.data.startswith("admin_oform_area_ru_"))
    dp.message.register(add_oform_photo_area, oform_ru.text_area)
    dp.message.register(add_oform_area_end, oform_ru.photo_area)

    dp.callback_query.register(oform_start_reff, F.data.startswith("admin_oform_reff_ru_"))
    dp.message.register(add_oform_photo_reff, oform_ru.text_reff)
    dp.message.register(add_oform_reff_end, oform_ru.photo_reff)

    dp.callback_query.register(oform_start_language, F.data.startswith("admin_oform_language_ru_"))
    dp.message.register(add_oform_photo_language, oform_ru.text_language)
    dp.message.register(add_oform_language_end, oform_ru.photo_language)

    dp.callback_query.register(oform_start_instuction, F.data.startswith("admin_oform_instuction_ru_"))
    dp.message.register(add_oform_photo_instuction, oform_ru.text_instruction)
    dp.message.register(add_oform_instruction_end, oform_ru.photo_instruction)

    dp.callback_query.register(oform_start_rules, F.data.startswith("admin_oform_rules_ru_"))
    dp.message.register(add_oform_photo_rules, oform_ru.text_rules)
    dp.message.register(add_oform_rules_end, oform_ru.photo_rules)

    dp.callback_query.register(oform_start_item, F.data.startswith("admin_oform_item_ru_"))
    dp.message.register(add_oform_photo_item, oform_ru.text_item)
    dp.message.register(add_oform_item_end, oform_ru.photo_item)

    dp.callback_query.register(add_oform_photo_profile, F.data.startswith("admin_oform_profile_ru_"))
    dp.message.register(add_oform_profile_end, oform_ru.photo_profile)

    dp.callback_query.register(oform_start_actcheck, F.data.startswith("admin_oform_actcheck_ru_"))
    dp.message.register(add_oform_photo_actcheck, oform_ru.text_actcheck)
    dp.message.register(add_oform_actcheck_end, oform_ru.photo_actcheck)

    dp.callback_query.register(oform_start_crypto, F.data.startswith("admin_oform_crypto_ru_"))
    dp.message.register(add_oform_photo_crypto, oform_ru.text_crypto)
    dp.message.register(add_oform_crypto_end, oform_ru.photo_crypto)

    dp.callback_query.register(oform_start_banc, F.data.startswith("admin_oform_banc_ru_"))
    dp.message.register(add_oform_photo_banc, oform_ru.text_banc)
    dp.message.register(add_oform_banc_end, oform_ru.photo_banc)

    dp.callback_query.register(oform_start_izbpokup, F.data.startswith("admin_oform_izbpokup_ru_"))
    dp.message.register(add_oform_photo_izbpokup, oform_ru.text_izbpokup)
    dp.message.register(add_oform_izbpokup_end, oform_ru.photo_izbpokup)
    dp.callback_query.register(copy_text, F.data.startswith("copy_text_"))

    dp.callback_query.register(oform_start_menu_en, F.data.startswith("admin_oform_start_menu_en_"))
    dp.message.register(add_oform_photo_menu_en, oform_en.text_menu)
    dp.message.register(add_oform_menu_end_en, oform_en.photo_menu)

    dp.callback_query.register(oform_start_city_en, F.data.startswith("admin_oform_city_en_"))
    dp.message.register(add_oform_photo_city_en, oform_en.text_city)
    dp.message.register(add_oform_city_end_en, oform_en.photo_city)

    dp.callback_query.register(oform_start_area_en, F.data.startswith("admin_oform_area_en_"))
    dp.message.register(add_oform_photo_area_en, oform_en.text_area)
    dp.message.register(add_oform_area_end_en, oform_en.photo_area)

    dp.callback_query.register(oform_start_language_en, F.data.startswith("admin_oform_language_en_"))
    dp.message.register(add_oform_photo_language_en, oform_en.text_language)
    dp.message.register(add_oform_language_end_en, oform_en.photo_language)

    dp.callback_query.register(oform_start_instuction_en, F.data.startswith("admin_oform_instuction_en_"))
    dp.message.register(add_oform_photo_instuction_en, oform_en.text_instruction)
    dp.message.register(add_oform_instruction_end_en, oform_en.photo_instruction)

    dp.callback_query.register(oform_start_rules_en, F.data.startswith("admin_oform_rules_en_"))
    dp.message.register(add_oform_photo_rules_en, oform_en.text_rules)
    dp.message.register(add_oform_rules_end_en, oform_en.photo_rules)

    dp.callback_query.register(oform_start_item_en, F.data.startswith("admin_oform_item_en_"))
    dp.message.register(add_oform_photo_item_en, oform_en.text_item)
    dp.message.register(add_oform_item_end_en, oform_en.photo_item)

    dp.callback_query.register(add_oform_photo_profile_en, F.data.startswith("admin_oform_profile_en_"))
    dp.message.register(add_oform_profile_end_en, oform_en.photo_profile)

    dp.callback_query.register(oform_start_actcheck_en, F.data.startswith("admin_oform_actcheck_en_"))
    dp.message.register(add_oform_photo_actcheck_en, oform_en.text_actcheck)
    dp.message.register(add_oform_actcheck_end_en, oform_en.photo_actcheck)

    dp.callback_query.register(oform_start_crypto_en, F.data.startswith("admin_oform_crypto_en_"))
    dp.message.register(add_oform_photo_crypto_en, oform_en.text_crypto)
    dp.message.register(add_oform_crypto_end_en, oform_en.photo_crypto)

    dp.callback_query.register(oform_start_blikwplata_en, F.data.startswith("wplata_oform_en"))
    dp.message.register(add_oform_photo_blikwplata_en, oform_en.text_blik_wplata)
    dp.message.register(add_oform_end_en_blik, oform_en.photo_blik_wplata)

    dp.callback_query.register(oform_start_banc_en, F.data.startswith("admin_oform_banc_en_"))
    dp.message.register(add_oform_photo_banc_en, oform_en.text_banc)
    dp.message.register(add_oform_banc_end_en, oform_en.photo_banc)

    dp.callback_query.register(oform_start_izbpokup_en, F.data.startswith("admin_oform_izbpokup_en_"))
    dp.message.register(add_oform_photo_izbpokup_en, oform_en.text_izbpokup)
    dp.message.register(add_oform_izbpokup_end_en, oform_en.photo_izbpokup)

    dp.callback_query.register(oform_start_reff_en, F.data.startswith("admin_oform_reff_en_"))
    dp.message.register(add_oform_photo_reff_en, oform_en.text_reff)
    dp.message.register(add_oform_reff_end_en, oform_en.photo_reff)



    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":

    asyncio.run(start())
