from zoneinfo import ZoneInfo

import httpx

from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State

import inline_button as ikb

from config import settings

from datetime import datetime


class AddTask(StatesGroup):
    title = State()
    category = State()
    date = State()


router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("👋 Добро пожаловать! Что вы хотите сделать?", reply_markup=ikb.menu)

@router.callback_query(F.data == "get_tasks")
async def get_tasks(cb: CallbackQuery):
    await cb.answer("")
    user_id = cb.from_user.id
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{settings.API_URL}tasks/?user={user_id}")
        if res.status_code == 200:
            tasks = res.json()

            if not tasks:
                await cb.message.answer("📭 У вас нет задач.")
                return

            text = "\n\n".join(
                f"📌 <b>{t.get('title', 'Без названия')}</b>\n"
                f"Категория: {t.get('category_name', 'Без категории')}\n"
                f"Создано: {str(t.get('created_at', '')[:16]).replace('T', ' ')}\n"
                f"Срок: {str(t.get('due_date', '')[:16]).replace('T', ' ')}"
                for t in tasks
            )
            await cb.message.answer(text)
        else:
            await cb.message.answer("⚠️ Ошибка сервера при получении задач.")

@router.callback_query(F.data == "add_task")
async def add_task_name(cb: CallbackQuery, state:FSMContext):
    await cb.answer("")
    await cb.message.answer("📝 Введите название задачи:")
    await state.set_state(AddTask.title)

@router.message(AddTask.title)
async def add_task_category(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AddTask.category)
    await message.answer("📂 Введите категорию задачи:")

@router.message(AddTask.category)
async def add_task_date(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await state.set_state(AddTask.date)
    await message.answer(" Введите дату исполнения (YYYY-MM-DD HH:MM):")


@router.message(AddTask.date)
async def add_task(message: Message, state: FSMContext):
    try:
        due_date = datetime.strptime(message.text, "%Y-%m-%d %H:%M")
    except ValueError:
            await message.answer("❌ Неверный формат. Используйте YYYY-MM-DD HH:MM")
            return
    data = await state.get_data()
    print(due_date.replace(tzinfo=ZoneInfo('America/Adak')))
    if due_date.replace(tzinfo=ZoneInfo('America/Adak')) < datetime.now(ZoneInfo('America/Adak')):
        await message.answer("❌ Нельзя создать задачу в прошлое.")
    else:
        payload = {
            "title": data['title'],
            "category": data["category"],
            "due_date": due_date.isoformat(),
            "user": message.from_user.id,
        }
        async with httpx.AsyncClient() as client:
            await client.post(f"{settings.API_URL}tasks/", json=payload)

        await message.answer("✅ Задача успешно создана!", reply_markup=ikb.menu)

