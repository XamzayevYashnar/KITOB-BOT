from aiogram import Router, F
from aiogram.types import Message
from default import *
from database import Database
from state import *
from aiogram.fsm.context import FSMContext

dp_1 = Router()
data = Database()
user_data = User()

@dp_1.message(F.text == "/register")
async def register_command(msg: Message, state: FSMContext):
    await msg.answer("Telefon raqamingizni yuboring\nMisol: +998...\nyoki tugmani bosing!", reply_markup=phone_button())
    await state.set_state(AddUser.phone_number)

@dp_1.message(F.contact, AddUser.phone_number)
async def contact_command(msg: Message):
    phone_number = msg.contact.phone_number
    user_id = msg.from_user.id
    username = msg.from_user.username
    user_data.add_user(user_id, username, phone_number)
    await msg.answer("Siz ro'yxatdan o'tdingiz!", reply_markup=menu_button())

@dp_1.message(AddUser.phone_number, F.text)
async def add_user_state(msg: Message):
    phone_number = msg.text
    user_id = msg.from_user.id
    username = msg.from_user.username
    if msg.text.startswith("+998"):
        user_data.add_user(user_id, username, phone_number)
        await msg.answer("Siz ro'yxatdan o'tdingiz!", reply_markup=menu_button())
    else:
        await msg.answer("Iltimos telefon raqamingizni +998 bilan boshlang!")
        return