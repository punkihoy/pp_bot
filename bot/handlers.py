from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
import bot.keyboards as kb
import os
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext

from bot.likes import LikesHandler, LikesState

router = Router()
load_dotenv("../config.env")



@router.message(CommandStart())
async def start_massage(message:Message):
    await message.answer(f"Привет, {message.from_user.first_name}, приятно тебя видеть!", reply_markup=kb.main_keyboard)


@router.message(F.text == "Мои лайки")
async def show_liked_posts(message: Message, state: FSMContext):
    likes_handler = LikesHandler(state)
    await likes_handler.show_liked_posts(message)

@router.callback_query(F.data == "next_like", LikesState.likes_data)
async def next_liked_post(callback: CallbackQuery, state: FSMContext):
    likes_handler = LikesHandler(state)
    await likes_handler.next_liked_post(callback)



@router.callback_query(F.data == "like")
async def like_message(callback:CallbackQuery):
    await callback.answer("Вы отметили сообщение")



@router.callback_query(F.data == "mode")
async def settings_mode(callback:CallbackQuery):
    pass
