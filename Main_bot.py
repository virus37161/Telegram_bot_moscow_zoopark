import asyncio

import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import F
from aiogram.utils.formatting import (
   Bold, as_list, as_marked_section
)

from tokens import TOKEN
from handlers import router
from aiogram.fsm.context import FSMContext

dp = Dispatcher()
dp.include_router(router)
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    kb = [[types.KeyboardButton(text="Команды"), types.KeyboardButton(text="Описание бота")]]
    keybord = (types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,))
    await message.answer (f"Добро пожаловать, дорогой друг!", reply_markup=keybord)

@dp.message(F.text.lower()=="команды")
async def main_comands(message:types.Message):
    responce = as_list(as_marked_section(Bold("Команды:"), f'/victorina - познакомиться со своим пушистым другом',
                                         f"/otziv - оставить отзыв",
                                         f'/opeka - наша программа опеки, которая улучшит твою и жизнь какого либо животного)',
                                         f'/support - связаться с сотрудником зоопарка',
                                         marker = "✅",))
    await message.answer(**responce.as_kwargs())



bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
async def main() -> None:
   await dp.start_polling(bot)

@dp.message(F.text =="Связаться со специалистом")
async def connect_support(message: types.Message):
    id = 6433843865
    await message.answer(f"@Aleks14242")
    await bot.send_message(chat_id=id, text = f"{message.chat.first_name}")

@dp.message(F.text =="Узнать, как взять под опеку вашего нового друга")
async def connect_support(message: types.Message):
    await message.answer(
        "По этой ссылке можно узнать информацию об опеке \nhttps://moscowzoo.ru/my-zoo/become-a-guardian/ \n"
        "А еще там очень много классных животных. Одного себе точно возьмете")

if __name__ == "__main__":
   logging.basicConfig(level=logging.INFO, stream=sys.stdout)
   asyncio.run(main())