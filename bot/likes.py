from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import sqlite3


class LikesState(StatesGroup):
    likes_data = State()
    current_like = State()


class LikesHandler:
    def __init__(self, state: FSMContext):
        self.state = state

    def get_liked_messages(self, user_id):
        conn = sqlite3.connect('texts.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT messages.id, messages.text FROM messages
            JOIN likes ON messages.id = likes.message_id
            WHERE likes.user_id = ?
        ''', (user_id,))
        liked_messages = [{"id": row[0], "text": row[1]} for row in cursor.fetchall()]
        conn.close()
        return liked_messages

    
    async def show_liked_posts(self, message: Message):
        liked_messages = self.get_liked_messages(message.from_user.id)

        if not liked_messages:
            await message.answer("Вы не поставили лайков на сообщения.")
            return

        await self.state.update_data(liked_messages=liked_messages)
        await self.state.set_state(LikesState.likes_data)

        current_message = liked_messages.pop(0)
        await message.answer(
            f"Лайкнутый пост: {current_message['text']}",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="➡️ Далее", callback_data="next_like")]
                ]
            )
        )
        await self.state.update_data(liked_messages=liked_messages)
        await self.state.update_data(current_like=current_message)

    async def next_liked_post(self, callback: CallbackQuery):
        data = await self.state.get_data()
        liked_messages = data["liked_messages"]

        if not liked_messages:
            await callback.answer("Это все ваши лайкнутые сообщения.")
            return

        current_message = liked_messages.pop(0)

        await callback.message.edit_text(
            f"Лайкнутый пост: {current_message['text']}",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="➡️ Далее", callback_data="next_like")]
                ]
            )
        )
        await self.state.update_data(liked_messages=liked_messages)
        await self.state.update_data(current_like=current_message)
