from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Искать"), KeyboardButton(text="Писать")],
    [KeyboardButton(text="Мои лайки")]
],
resize_keyboard=True,
input_field_placeholder="Выберите действие...")


watch_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="♥", callback_data="like") ,InlineKeyboardButton(text="->", callback_data="next")],
    []
])

watch_keyboard_past = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="♥", callback_data="like")]
])

# write_keyboard = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="Отправить", callback_data="")],
#     [InlineKeyboardButton(text="Отменить", callback_data="")]
# ])

settings_keyboard =  InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Режим", callback_data = "mode")],
    [InlineKeyboardButton(text="Контакт", callback_data = "ddd")]
])

admin_main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Блок", callback_data="block_user"), InlineKeyboardButton(text="Разблок", callback_data="unblock_user")],
   [InlineKeyboardButton(text="Режим", callback_data="mode")]
])

success_keyboard = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Отправить", callback_data="succes_write")],
   [InlineKeyboardButton(text="Отменить", callback_data="cancel_write")]
])

cancel_keyboard  = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Отменить", callback_data="cancel_write")]
])
