from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from default import *
from database import *
from state import *
from inline import *

router = Router()
data = Database()
user_data = User()
cart = Cart()
ADMINS = [7888427770]

@router.message(Command("start"))
async def start_command(msg: Message):
    if user_data.check_users(msg.from_user.id):
            await msg.answer("⛑️ Bosh menyu", reply_markup=menu_button())
    else:
        await msg.answer("Iltimos avval ro'yxatdan o'ting! (/register) dan o'ting")
        return

@router.message(F.text == "📕 KITOBLAR")
async def get_books(msg: Message, state: FSMContext):
    result = get_categorie_buttons()
    await msg.answer("KATEGORIYALARDAN BIRINI TANLANG", reply_markup=result)
    await state.set_state(ForButton.activate1)


@router.message(ForButton.activate1, F.text)
async def get_products(msg: Message, state: FSMContext):
    result = get_book_buttons(msg.text)
    if result:
        await msg.answer("KITOBLARDAN BIRINI TANLANG", reply_markup=result)
        await state.set_state(ForButton.activate3)
    else:
        await msg.answer("🥲 Afsuski kitoblar xali kiritilmagan")
        await state.clear()

@router.message(ForButton.activate3, F.text)
async def get_book(msg: Message):
    result = cat_data.get_books_for_name(msg.text)
    if result is not None:
        await msg.answer_photo(
            result[4],
            caption=f"""📖 Kitob nomi: {result[2]}
    💰 Narxi: {result[5]} so'm
    ✍️ Muallifi: {result[6]}
    📝 Sarlavha: {result[7]}"""
        , reply_markup=add_cart_buttons(1, result[0]))
    else:
        return

@router.callback_query(F.data == "minus_count")
async def minus_count(callback: CallbackQuery):
    count = int(callback.message.reply_markup.inline_keyboard[0][1].text)
    print(count)
    if count > 1:
        count -= 1
        await callback.message.edit_reply_markup(reply_markup=add_cart_buttons(count=count,
                                product_id=callback.message.reply_markup.inline_keyboard[0][1].callback_data.split("_")[1]))
    else:
        await callback.answer("Soni 1 dan kam bo'lishi mumkin emas!")

@router.callback_query(F.data == "plus_count")
async def plus_count(callback: CallbackQuery):
    count = int(callback.message.reply_markup.inline_keyboard[0][1].text)
    print(count)
    count += 1
    await callback.message.edit_reply_markup(reply_markup=add_cart_buttons(count=count,
                                product_id=callback.message.reply_markup.inline_keyboard[0][1].callback_data.split("_")[1]))

@router.callback_query(F.data == "add_to_cart")
async def cart_button(call: CallbackQuery):
    product_id = call.message.reply_markup.inline_keyboard[0][1].callback_data.split("_")[1]
    user_id = call.from_user.id
    natija = cat_data.get_books_for_id_product(product_id)
    print(user_id)

    if natija is not None:
        narxi = int(natija[5])
        nomi = natija[3]
        count = int(call.message.reply_markup.inline_keyboard[0][1].text)
        umumiy_narx = narxi * count
        author = natija[6]
        cart.add_cart(user_id, product_id, nomi, count, umumiy_narx, author)

        await call.message.answer(
            f"Mahsulot savatingizga qo‘shildi!\n"
            f"Soni: {count} dona\n"
            f"Narxi: {narxi}\n"
            f"Umumiy narxi: {umumiy_narx} so'm\n"
            f"Mahsulot: {nomi}", reply_markup=menu_button()
        )
        bk.add_order(user_id, nomi, count, narxi, umumiy_narx, author)

        await call.message.edit_reply_markup(reply_markup=add_cart_buttons(1, product_id))
    else:
        await call.message.answer("Mahsulot topilmadi yoki xatolik yuz berdi.")

@router.message(F.text == "🧺 SAVATCHA")
async def get_buyurtmalar(msg: Message):
    result = cart.get_cart(msg.from_user.id)
    total_price = 0
    if result:
        for i in result:
            await msg.answer(f""" 
            📚 Kitob nomi: {i[2]}
            📦 Olingan donasi: {i[3]}
            💸 Dona narxi: {i[4]}
            💰 Umumiy narxi: {i[5]}
            ✍️ Muallifi: {i[6]}
            """)
            total_price += int(i[5])
        await msg.answer(f"Savatdagi mahsulotlarni jami narx: {total_price} s'om", reply_markup=buuy_product())
        await msg.answer("🔚 BU SIZNI OLGAN BARCHA KITOBLARIZ")
    else:
        await msg.answer("Siz hali hech nima buyurtma qilmagansiz.", reply_markup=menu_button())

@router.callback_query(F.data == "buy_product")
async def buy_command(call: CallbackQuery):
    if cat_data.check_order(call.from_user.id):
        await call.message.answer("Manzilni yuborish:", reply_markup=location_func())
    else:
        await call.message.answer("Siz xali hech nima olganiz yuq")

@router.message(F.location)
async def location_handler(msg: Message):
    latitude = msg.location.latitude
    longitude = msg.location.longitude
    username = msg.from_user.username
    user_id = msg.from_user.id
    phone_number = user_data.get_phone_number(user_id)[0]
    info_product = bk.get_orders(user_id)
    product_name = info_product[2][1]
    count = info_product[3][0]
    one_price = info_product[4][0]
    total_price = info_product[5][0]
    cart.add_history(user_id, username, phone_number, latitude, longitude, product_name, one_price, total_price, count)
    await msg.answer("Mahsulotlariz tez orada yetkazib beriladi!")
    bk.delete_cart(msg.from_user.id)
