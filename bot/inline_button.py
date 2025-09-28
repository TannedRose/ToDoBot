from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardBuilder

menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="➕ Добавить задачу", callback_data="add_task")],
    [InlineKeyboardButton(text="📋 Посмотреть задачи", callback_data="get_tasks")],
])
