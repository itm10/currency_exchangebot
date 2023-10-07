import asyncio
import os

from aiogram import Bot
from aiogram.types import Message
from aiogram.filters import CommandStart
from dispatchers import dp
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext
from code import currency_data
from commands import start,help,currency, wikipedias
from states import UserState
import wikipedia

load_dotenv()


@dp.message(CommandStart())
async def start_bot(message: Message):
    first_name = message.from_user.first_name
    await message.answer(f'Hello {first_name}!\nChoose /currency to see real time currency exchange')


@dp.message(lambda msg: msg.text == '/currency')
async def get_currency(message: Message, state: FSMContext):
    await message.answer('Enter currency that you currently hold. Must be 3-character currency code (e.g. USD).')
    await state.set_state(UserState.have)


@dp.message(UserState.have)
async def want_get(message: Message, state: FSMContext):
    having = message.text
    await state.update_data({
        'have': having
    })
    await message.answer('Enter currency you want to convert to. Must be 3-character currency code (e.g. EUR)')
    await state.set_state(UserState.want)


@dp.message(UserState.want)
async def final_stage(message: Message, state: FSMContext):
    want = message.text
    await state.update_data({
        'want': want
    })
    await message.answer('Enter amount of currency to convert.')
    await state.set_state(UserState.value)


@dp.message(UserState.value)
async def get_value(message: Message, state: FSMContext):
    value = message.text
    data = await state.get_data()
    have = data['have']
    want = data['want']
    try:
        answer = currency_data(have, want, int(value))
        await message.answer(f'Currency exchange: {value}{have} => {answer}{want}')
        await message.answer('Choose /currency to enter new currency exchange')
        await state.storage.close()
        await state.clear()
    except:
        await message.answer('You entered wrong currency code')
        await state.storage.close()
        await state.clear()
        await message.answer('Try again!  /currency')


@dp.message(UserState.wikitext)
async def wiki_get(message: Message, state: FSMContext):
    response=message.text
    await state.update_data({
        'wikitext': response
    })
    await message.answer('Enter a language of wikipedia text (like en, ru...)')
    await state.set_state(UserState.langes)


@dp.message(UserState.langes)
async def lang_wiki(message: Message, state: FSMContext):
    lang=message.text
    data=await state.get_data()
    responses=data['wikitext']
    try:
        wikipedia.set_lang(lang)
        answer=wikipedia.summary(responses)
        await message.answer(answer)
        await state.storage.close()
        await state.clear()
    except:
        await message.answer('Not found')
        await message.answer('Try again! /wikipedia')


@dp.message(lambda msg: msg.text=='/wikipedia')
async def again_wik(message:Message, state:FSMContext):
    await message.answer('Enter a text: ')
    await state.set_state(UserState.wikitext)






async def main():
    t=os.getenv('TOKEN')
    bot=Bot(t)
    await bot.set_my_commands([start,help,currency, wikipedias])
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
