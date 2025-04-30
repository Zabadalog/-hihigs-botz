import pytest
from handlers.handlers import callback_continue
from fixtures import mock_callback, mock_message

@pytest.mark.asyncio
async def test_callback_continue(mock_callback):
    # Вызываем коллбэк-хэндлер с корректным объектом CallbackQuery
    await callback_continue(mock_callback)

    # Проверяем, что answer был вызван у прикрепленного сообщения
    mock_callback.message.answer.assert_awaited_once_with(text="Успешно вызван callback!")
