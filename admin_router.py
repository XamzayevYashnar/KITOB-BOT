from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from default import *
from database import *
from state import AddBook, AddCategorie, Activate1, Activate2, Activate3
from inline import add_cart_buttons

rt = Router()

data = Database()
user_data = User()
cart = Cart()
bk = Book()
cat_data = Categories()

ADMINS = [7888427770]

@rt.message(Command("admin"))
async def admin_panel(msg: Message):
    if msg.from_user.id in ADMINS:
        await msg.answer("ADMIN PANEL", reply_markup=admin_button())

@rt.message(F.text == "➕ ADD BOOK")
async def add_book(msg: Message, state: FSMContext):
    await msg.answer("Kitob nomini kiriting\nMisol: GariPoter")
    await state.set_state(AddBook.name)

@rt.message(AddBook.name)
async def get_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("Kitobning rasmini yuboring")
    await state.set_state(AddBook.image)

@rt.message(F.photo, AddBook.image)
async def get_photo(msg: Message, state: FSMContext):
    file_id = msg.photo[-1].file_id
    await state.update_data(image=file_id)
    await msg.answer("Kitobni narxini kiriting\nMisol: 50_000")
    await state.set_state(AddBook.price)

@rt.message(AddBook.price)
async def get_price(msg: Message, state: FSMContext):
    await state.update_data(price=msg.text)
    await msg.answer("Kitob muallifini kiriting")
    await state.set_state(AddBook.aythor)

@rt.message(AddBook.aythor)
async def get_aythor(msg: Message, state: FSMContext):
    await state.update_data(aythor=msg.text)
    await msg.answer("Kitob sarlavhasini kiriting\n(Qisqa ma'lumot)")
    await state.set_state(AddBook.sarlavha)

@rt.message(AddBook.sarlavha)
async def get_sarlavha(msg: Message, state: FSMContext):
    await state.update_data(sarlavha=msg.text)
    button = get_categorie_buttons()
    await msg.answer("QAYSI KATEGORIYAGA QO‘SHMOQCHISIZ?", reply_markup=button)
    await state.set_state(Activate3.activate)

@rt.message(Activate3.activate, F.text)
async def get_categorie(msg: Message, state: FSMContext):
    data_dict = await state.get_data()
    categorie_name = msg.text
    res = cat_data.check_categorie(categorie_name)
    if not res:
        await msg.answer("Bunday kategoriya topilmadi.")
        return

    categorie_id = res[0]
    name = data_dict.get("name")
    image = data_dict.get("image")
    price = data_dict.get("price")
    aythor = data_dict.get("aythor")
    sarlavha = data_dict.get("sarlavha")

    await msg.answer(f""" 
Kitob nomi: {name}
Kitob narxi: {price}
Kitob muallifi: {aythor}
Sarlavha: {sarlavha}
Kategoriya ID: {categorie_id}
Kategoriya nomi: {categorie_name}
""")
    bk.add_book(categorie_id, categorie_name, name, image, price, aythor, sarlavha)
    await msg.answer("🙆‍♂️ Ma'lumot qo‘shildi")
    await state.clear()

@rt.message(F.text == "🧾 GET BOOKS")
async def get_books(msg: Message, state: FSMContext):
    await msg.answer("KATEGORIYALARDAN BIRINI TANLANG", reply_markup=get_categorie_buttons())
    await state.set_state(Activate2.activate)

@rt.message(Activate2.activate, F.text)
async def activate_books(msg: Message, state: FSMContext):
    categorie_name = msg.text
    result = get_book_buttons(categorie_name)
    if not result:
        await msg.answer("Ushbu kategoriya bo‘sh yoki mavjud emas.")
        return
    await msg.answer(f"{categorie_name} ga tegishli kitoblar:", reply_markup=result)
    await state.set_state(Activate1.activate)

@rt.message(Activate1.activate, F.text)
async def activate_books_detail(msg: Message, state: FSMContext):
    result = cat_data.get_books_for_name(msg.text)
    if not result:
        await msg.answer("Kitob kiritilmagan")
        await state.clear()
        return


    await msg.answer_photo(
        result[4],
        caption=f"""📖 Kitob nomi: {result[3]}
💰 Narxi: {result[5]} so'm
✍️ Muallifi: {result[6]}
📝 Sarlavha: {result[7]}""",
            reply_markup=add_cart_buttons(1, result[0])
        )
    await state.clear()

@rt.callback_query(F.data == "minus_count")
async def minus_count(callback: CallbackQuery):
    count = int(callback.message.reply_markup.inline_keyboard[0][1].text)
    if count > 1:
        count -= 1
        await callback.message.edit_reply_markup(
            reply_markup=add_cart_buttons(count, callback.message.reply_markup.inline_keyboard[0][1].callback_data.split("_")[1])
        )
    else:
        await callback.answer("Soni 1 dan kam bo'lishi mumkin emas!")

@rt.callback_query(F.data == "plus_count")
async def plus_count(callback: CallbackQuery):
    count = int(callback.message.reply_markup.inline_keyboard[0][1].text)
    count += 1
    await callback.message.edit_reply_markup(
        reply_markup=add_cart_buttons(count, callback.message.reply_markup.inline_keyboard[0][1].callback_data.split("_")[1])
    )

@rt.callback_query(F.data == "add_to_cart")
async def cart_button(call: CallbackQuery):
    product_id = call.message.reply_markup.inline_keyboard[0][1].callback_data.split("_")[1]
    user_id = call.from_user.id
    result = bk.get_books_by_id(user_id)

    if result:
        name = result[3]
        price = int(result[5])
        author = result[6]
        count = int(call.message.reply_markup.inline_keyboard[0][1].text)
        total_price = price * count

        cart.add_cart(user_id, name, count, price, total_price, author)
        await call.message.answer(
            f"Mahsulot savatingizga qo‘shildi!\n"
            f"Soni: {count} dona\n"
            f"Umumiy narxi: {total_price} so'm\n"
            f"Mahsulot: {name}", reply_markup=menu_button()
        )
        await call.message.edit_reply_markup(reply_markup=add_cart_buttons(1, product_id))
    else:
        await call.message.answer("Mahsulot topilmadi yoki xatolik yuz berdi.")

@rt.message(F.text == "➕ ADD CATEGORIE")
async def add_categorie(msg: Message, state: FSMContext):
    await msg.answer("KATEGORIYA NOMINI KIRITING")
    await state.set_state(AddCategorie.categorie)

@rt.message(AddCategorie.categorie, F.text)
async def add_categorie_final(msg: Message, state: FSMContext):
    cat_data.add_categorie(msg.text)
    await msg.answer("✅ Kategoriya yaratildi!")
    await state.clear()


