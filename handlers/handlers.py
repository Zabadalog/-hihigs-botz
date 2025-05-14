import logging
import secrets
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select

from db import async_session
from db.models import User
from handlers.keyboard import main_keyboard_start

router = Router()

class RegisterStates(StatesGroup):
    choosing_role = State()
    entering_tutor_code = State()

@router.message(Command("start"))
async def process_start_command(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Выберите вашу роль:", reply_markup=main_keyboard_start)
    await state.set_state(RegisterStates.choosing_role)

@router.message(Command("status"))
async def process_status_command(message: types.Message):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.user_id == message.from_user.id))
        user = result.scalar_one_or_none()

        if not user:
            await message.answer("Вы не зарегистрированы. Нажмите /start")
            return

        if user.tutorcode:
            await message.answer(
                f"Вы — преподаватель:\n"
                f"ID: {user.user_id}\n"
                f"Username: @{user.username or 'не задан'}\n"
                f"Код для студентов: `{user.tutorcode}`",
                parse_mode="Markdown"
            )
        elif user.subscribe:
            # получаем данные преподавателя
            result = await session.execute(select(User).where(User.user_id == user.subscribe))
            teacher = result.scalar_one_or_none()

            if teacher:
                await message.answer(
                    f"Вы — слушатель:\n"
                    f"ID: {user.user_id}\n"
                    f"Username: @{user.username or 'не задан'}\n"
                    f"Подписан на преподавателя: @{teacher.username or 'не задан'}"
                )
            else:
                await message.answer(
                    f"Вы — слушатель, но преподаватель с ID {user.subscribe} не найден."
                )
        else:
            await message.answer("Невозможно определить ваш статус.")


@router.message(Command("help"))
async def process_help_command(message: types.Message):
    await message.answer("Напишите /start, чтобы зарегистрироваться.\nНапишите /status, чтобы узнать статус.")

@router.callback_query(F.data == "button_student")
async def handle_student(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите код преподавателя (введите текстом):")
    await state.set_state(RegisterStates.entering_tutor_code)
    await callback.answer()

@router.message(RegisterStates.entering_tutor_code)
async def process_tutor_code(message: types.Message, state: FSMContext):
    code = message.text.strip()

    async with async_session() as session:
        result = await session.execute(select(User).where(User.tutorcode == code))
        tutor = result.scalar_one_or_none()

        if tutor:
            existing = await session.execute(select(User).where(User.user_id == message.from_user.id))
            user_obj = existing.scalar_one_or_none()

            if user_obj:
                user_obj.subscribe = tutor.user_id
                user_obj.tutorcode = None
            else:
                session.add(User(
                    user_id=message.from_user.id,
                    username=message.from_user.username or "no_username",
                    subscribe=tutor.user_id
                ))

            await session.commit()
            await message.answer(f"Вы зарегистрированы как слушатель преподавателя @{tutor.username}")
            await state.clear()
        else:
            await message.answer("Неверный код. Попробуйте снова:")


@router.callback_query(F.data == "button_tutor")
async def handle_tutor(callback: types.CallbackQuery, state: FSMContext):
    user = callback.from_user
    tutorcode = f"TUT{user.id}"
    username_value = user.username or "no_username"

    async with async_session() as session:
        result = await session.execute(select(User).where(User.user_id == user.id))
        existing = result.scalar_one_or_none()

        if existing:
            existing.tutorcode = tutorcode
            existing.subscribe = None
        else:
            session.add(User(
                user_id=user.id,
                username=username_value,
                tutorcode=tutorcode
            ))
            await session.commit()

    await callback.message.answer(
        f"Вы выбрали роль: *Преподаватель*.\n\n"
        f"Ваш ID: `{user.id}`\n"
        f"Username: @{user.username or '—'}\n"
        f"Код преподавателя: `TUT{user.id}`",
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message()
async def echo_message(message: types.Message):
    await message.answer(f"Вы написали: {message.text}")
