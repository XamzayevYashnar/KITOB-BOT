from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database import *

cat_data = Categories()
bk = Book()

def menu_button():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📕 KITOBLAR")],
            [KeyboardButton(text="🧺 SAVATCHA"), KeyboardButton(text="🧾 BUYURTMALARIM")]
        ],
        resize_keyboard=True
    )

def admin_button():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="➕ ADD BOOK"),
                KeyboardButton(text="➕ ADD CATEGORIE"),
                KeyboardButton(text="🧾 GET BOOKS")
            ]
        ],
        resize_keyboard=True
    )

def phone_button():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True)]
        ],
        resize_keyboard=True
    )

def get_categorie_buttons():
    result = cat_data.get_categories_for_button()
    if result:
        buttons = [
            [KeyboardButton(text=cat[1]) for cat in result[i:i + 2]]
            for i in range(0, len(result), 2)
        ]
        return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    else:
        return ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Malumot topilmadi")]],
            resize_keyboard=True
        )


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_book_buttons(category_name):
    result = cat_data.mt_books(category_name)
    buttons = []

    for book in result:
        if book[3]:  # Agar book[3] None bo‘lmasa
            buttons.append([KeyboardButton(text=str(book[3]))])

    if not buttons:
        return None

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def location_func():
    button = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🗝️ Manzuilni yuborish", request_location=True)
            ]
        ], resize_keyboard=True
    )
    return button