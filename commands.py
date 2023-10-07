from aiogram.types import BotCommand, Message
from aiogram.filters.command import Command
from dispatchers import dp
from aiogram.fsm.context import FSMContext
from states import UserState

start=BotCommand(command='start', description='start a bot')
help=BotCommand(command='help', description='help commmand')
currency=BotCommand(command='currency', description='currency exchange')
wikipedias=BotCommand(command='wikipedia', description='wikipedia informations')

@dp.message(Command(help))
async def help_command(message: Message):
    await message.answer('You can control me by sending these commands:\n\n'
                         '/start - start a bot\n'
                         '/help - get a guide\n'
                         '/currency - currency exchange\n'
                         '/wikipedia - wikipedia informations')


@dp.message(Command(currency))
async def currency_command(message:Message, state:FSMContext):
    await message.answer('Enter currency that you currently hold. Must be 3-character currency code (e.g. USD).')
    await message.delete()
    await state.set_state(UserState.have)


@dp.message(Command(wikipedias))
async def wikipedia(message: Message, state:FSMContext):
    await message.answer('Enter a text: ')
    await state.set_state(UserState.wikitext)
