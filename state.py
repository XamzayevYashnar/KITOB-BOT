from aiogram.fsm.state import StatesGroup, State

class AddUser(StatesGroup):
    phone_number = State()

class AddBook(StatesGroup):
    name = State()
    image = State()
    price = State()
    aythor = State()
    sarlavha = State()
    categorie = State()

class ActivayeButtons(StatesGroup):
    activate = State()

class AddCategorie(StatesGroup):
    categorie = State()

class Activate1(StatesGroup):
    activate = State()

class Activate2(StatesGroup):
    activate = State()

class Activate3(StatesGroup):
    activate = State()

class Activate4(StatesGroup):
    activate = State()


class ForButton(StatesGroup):
    activate1 = State()
    activate2 = State()
    activate3 = State()