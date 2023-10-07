from aiogram.filters.state import State, StatesGroup

class UserState(StatesGroup):
    have=State()
    want=State()
    value=State()
    wikitext=State()
    langes=State()