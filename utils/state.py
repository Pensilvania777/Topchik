from aiogram.fsm.state import StatesGroup, State


class Rass(StatesGroup):
    rass_text = State()
    rass_photo = State()


class City(StatesGroup):
    city_add = State()
    city_del = State()

class Admin(StatesGroup):
    admin_name = State()
    admin_id = State()

class Area(StatesGroup):
    name_area = State()

class Item(StatesGroup):
    name_item = State()
    name_opis = State()
    price_item = State()
    photo_item = State()

class Gram(StatesGroup):
    name_gram = State()

class Balance(StatesGroup):
    external_id = State()
    balance_summ = State()

class Balance_del(StatesGroup):
    balance_del = State()
    external_id_del = State()

class Clad(StatesGroup):
    city_clad = State()
    latit = State()
    longtit = State()
    longdob = State()
    photo_clad = State()
    del_clad = State()

class Asset_summ(StatesGroup):
    summ_asset = State()


class Captcha(StatesGroup):
    captcha = State()
    text_cp = State()

class Blik(StatesGroup):
    summ_blick = State()

class Comment(StatesGroup):
    comment = State()

class Dispute(StatesGroup):
    dispute_text = State()
    dispute_photo = State()

class CladMan(StatesGroup):
    name_cladman = State()
    external_id_cladman = State()

class CladManJob(StatesGroup):
    city_clad = State()
    latit = State()
    longtit = State()
    longdob = State()
    photo_clad = State()
    del_clad = State()

class Blick_payment(StatesGroup):
    summ_blick = State()
    check_end = State(
    )

class oform_ru(StatesGroup):
    text_menu = State()
    photo_menu = State()
    text_city = State()
    photo_city = State()
    text_area = State()
    photo_area = State()
    text_language = State()
    photo_language = State()
    text_instruction = State()
    photo_instruction = State()
    text_rules = State()
    photo_rules = State()
    text_profile = State()
    photo_profile = State()
    text_item = State()
    photo_item = State()
    text_actcheck = State()
    photo_actcheck = State()
    text_crypto = State()
    photo_crypto = State()
    text_blik_number = State()
    text_blik_wplata = State()
    photo_blik_number = State()
    photo_blik_wplata = State()
    text_iban = State()
    text_number_phone = State()
    text_name_poluch = State()
    text_banc = State()
    photo_banc = State()
    text_izbpokup = State()
    photo_izbpokup = State()
    text_reff = State()
    photo_reff = State()

class oform_en(StatesGroup):
    text_menu = State()
    photo_menu = State()
    text_city = State()
    photo_city = State()
    text_area = State()
    photo_area = State()
    text_language = State()
    photo_language = State()
    text_instruction = State()
    photo_instruction = State()
    text_rules = State()
    photo_rules = State()
    text_profile = State()
    photo_profile = State()
    text_item = State()
    photo_item = State()
    text_actcheck = State()
    photo_actcheck = State()
    text_crypto = State()
    photo_crypto = State()
    text_blik_number = State()
    text_blik_wplata = State()
    photo_blik_number = State()
    photo_blik_wplata = State()
    text_banc = State()
    photo_banc = State()
    text_izbpokup = State()
    photo_izbpokup = State()
    text_reff = State()
    photo_reff = State()

