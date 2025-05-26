from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def add_cart_buttons(count, product_id):
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➖", callback_data="minus_count"),
                InlineKeyboardButton(text=str(count), callback_data=f"count_{product_id}"),
                InlineKeyboardButton(text="➕", callback_data="plus_count"),
            ],
            [
                InlineKeyboardButton(text="🗑 Savatchaga qo'shish", callback_data="add_to_cart")
            ]
        ]
    )
    return buttons

def buuy_product():
    button = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Mahsulotni xarid qilib olish", callback_data="buy_product")
            ]
        ]
    )
    return button
