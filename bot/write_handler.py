from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
import bot.keyboards as kb
from dotenv import load_dotenv
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import sqlite3

conn = sqlite3.connect('texts.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS likes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id INTEGER,
        user_id INTEGER,
        UNIQUE(message_id, user_id)  -- Чтобы один пользователь мог лайкнуть только один раз
    )
''')

conn.commit()
conn.close()


router_write = Router()
load_dotenv("../config.env")


class WritePost(StatesGroup):
    id = State()
    text_post = State()
    success = State()


@router_write.message(F.text == "Писать")
async def write_mode(message: Message, state:FSMContext):
    await message.answer(f"Напишите свое посланиe...", reply_markup=kb.cancel_keyboard)
    await state.set_state(WritePost.text_post)


@router_write.message(WritePost.text_post)
async def writer(message:Message, state:FSMContext):
    if len(message.text) <= 10 and len(message.text.split(" ")) < 3:
        await message.answer(f"Сообщение слишком короткое", reply_markup=kb.cancel_keyboard)
    else:
        await state.update_data(id = message.from_user.id)
        await state.update_data(text_post = message.text)
        await message.reply(f"Отправить?", reply_markup=kb.success_keyboard)
        await state.set_state(WritePost.success)


@router_write.callback_query(F.data == "succes_write", WritePost.success)
async def add_db(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    conn = sqlite3.connect('texts.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (user_id, text) VALUES (?, ?)",
                   (data['id'], data['text_post']))
    conn.commit()
    conn.close()

    await callback.answer("Отправлено")
    await callback.message.edit_text("Сообщение отправлено в полет")
    await state.clear()
    

@router_write.callback_query(F.data == "cancel_write", WritePost.success)
async def cancel_write(callback:CallbackQuery, state:FSMContext):
    await callback.answer("Отмена")
    await callback.message.edit_text(f"Отправка сообщения отменена")
    await state.clear()


@router_write.callback_query(F.data == "cancel_write", WritePost.text_post)
async def cancel_write(callback:CallbackQuery, state:FSMContext):
    await callback.answer("Отмена")
    await callback.message.edit_text(f"Написание сообщения отменено")
    await state.clear()


@router_write.callback_query(F.data == "cancel_write")
async def cancel_write(callback:CallbackQuery, state:FSMContext):
    await callback.answer("")
    await callback.message.edit_reply_markup(reply_markup=None)

  



    
