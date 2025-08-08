from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F, Router
import sqlite3
from dotenv import load_dotenv
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router_watch = Router()
load_dotenv("../config.env")


class WatcherState(StatesGroup):
    data_full = State()
    last_message_id = State()


def get_random_messages(user_id):
    conn = sqlite3.connect('texts.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, text FROM messages 
        WHERE id NOT IN (SELECT message_id FROM likes WHERE user_id = ?)
        ORDER BY RANDOM() LIMIT 10
    ''', (user_id,))
    messages = [{"id": row[0], "text": row[1]} for row in cursor.fetchall()]
    conn.close()
    return messages


def get_likes_count(message_id):
    conn = sqlite3.connect('texts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM likes WHERE message_id = ?", (message_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count


def like_message(user_id, message_id):
    """ Ставим лайк сообщению (если его ещё нет) """
    conn = sqlite3.connect('texts.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO likes (message_id, user_id) VALUES (?, ?)", (message_id, user_id))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Если лайк уже есть, ничего не делаем
    conn.close()


def generate_keyboard(message_id):
    like_count = get_likes_count(message_id)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"❤️ {like_count}", callback_data=f"like_{message_id}")],
            [InlineKeyboardButton(text="➡️ Далее", callback_data="next")]
        ]
    )
    return keyboard


@router_watch.message(F.text == "Искать")
async def search_mode(message: Message, state: FSMContext):
    await state.clear()
    messages = get_random_messages(message.from_user.id)

    if not messages:
        sent_message = await message.answer("Сообщений пока нет.", reply_markup=None)
        await state.update_data(last_message_id=sent_message.message_id)
        return

    await state.update_data(data_texts=messages)
    await state.set_state(WatcherState.data_full)

    mess = await state.get_data()
    current_message = mess["data_texts"].pop()

    sent_message = await message.answer(
        f'{current_message["text"]}', reply_markup=generate_keyboard(current_message["id"])
    )
    await state.update_data(last_message_id=sent_message.message_id)


@router_watch.callback_query(F.data.startswith("like_"), WatcherState.data_full)
async def like_post(callback: CallbackQuery, state: FSMContext):
    message_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    conn = sqlite3.connect('texts.db')
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM likes WHERE message_id = ? AND user_id = ?", (message_id, user_id))
    already_liked = cursor.fetchone()

    if already_liked:
        cursor.execute("DELETE FROM likes WHERE message_id = ? AND user_id = ?", (message_id, user_id))
    else:
        cursor.execute("INSERT INTO likes (message_id, user_id) VALUES (?, ?)", (message_id, user_id))

    conn.commit()
    conn.close()

    await callback.message.edit_reply_markup(reply_markup=generate_keyboard(message_id))

    action = "Лайк убран!" if already_liked else "Вы поставили лайк!"
    await callback.answer(action)



@router_watch.callback_query(F.data == "next", WatcherState.data_full)
async def next_message(callback: CallbackQuery, state: FSMContext):
    mess = await state.get_data()

    if len(mess["data_texts"]) == 0:
        messages = get_random_messages(callback.from_user.id)
        if not messages:
            await callback.answer("Больше сообщений нет.", show_alert=True)
            return
        await state.update_data(data_texts=messages)
        mess = await state.get_data()

    current_message = mess["data_texts"].pop()

    await callback.message.edit_text(
        f"{current_message['text']}", reply_markup=generate_keyboard(current_message["id"])
    )
