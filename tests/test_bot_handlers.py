import pytest
from fixtures import mock_message, mock_router
from handlers.handlers import process_help_command, process_start_command
from aiogram.types import InlineKeyboardMarkup

@pytest.mark.asyncio
async def test_process_help_command(mock_router, mock_message):
    # # Вызываем хендлер
    await process_help_command(mock_message)

    # # Проверка, что mock_message был вызван
    assert mock_message.answer.called, "message.answer не был вызван"

    # Проверяем, что mock_ был вызван один раз с ожидаемым результатом
    mock_message.answer.assert_called_once_with(text="ПОМОГИ!")

@pytest.mark.asyncio
async def test_process_start_command(mock_router, mock_message):
    # # Вызываем хендлер
    await process_start_command(mock_message)

    # # Проверка, что mock_message был вызван
    assert mock_message.reply.called, "message.reply не был вызван"

    # параметры, с которыми был вызван хендлер
    called_args, called_kwargs = mock_message.reply.call_args

    # проверка корректности текста
    expected_text = f'ID{mock_message.from_user.id}, User: {mock_message.from_user.username}'
    assert called_args[0] == expected_text

    # Вызываем клавиатуру
    markup = called_kwargs["reply_markup"]
    assert isinstance(markup, InlineKeyboardMarkup), "reply_markup не является Inline-клавиатурой"

    # Проверяем, что mock_ был вызван один раз с ожидаемым результатом
    # mock_message.answer.assert_called_once_with(text="ПОМОГИ!")
