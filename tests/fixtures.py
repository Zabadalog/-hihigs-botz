import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import Message
from aiogram import Router
from aiogram.types import CallbackQuery

# Фикстуры в pytest позволяют выносить в отдельные функции типовые действия
# например: настройка тестового окружения, создание тестовых данных, выполнение завершающие действия
# https://habr.com/ru/articles/731296/

@pytest.fixture
def mock_bot():
    """Mock бот"""
    with patch("main.Bot") as mock_bot_cls:
        mock_bot_instance = AsyncMock()
        mock_bot_cls.return_value = mock_bot_instance
        yield mock_bot_instance

@pytest.fixture
def mock_set_my_commands():
    """Mock создание меню"""
    with patch("main.set_my_commands", new_callable=AsyncMock) as mock:
        yield mock_set_my_commands

@pytest.fixture
def mock_dispatcher():
    """Mock диспетчер"""
    with patch("main.Dispatcher") as mock_dispatcher_cls:
        mock_dispatcher_instance = AsyncMock()
        mock_dispatcher_instance.start_polling = AsyncMock()
        mock_dispatcher_instance.include_routers = AsyncMock()
        mock_dispatcher_cls.return_value = mock_dispatcher_instance
        yield mock_dispatcher_instance

@pytest.fixture
def mock_set_up_logger():
    """Mock логгер"""
    with patch("main.set_up_logger", new_callable=AsyncMock) as mock:
        yield mock_set_up_logger

@pytest.fixture
def mock_message():
    """Mock сообщение"""
    mock_msg = AsyncMock(spec=Message)
    mock_msg.from_user = AsyncMock()
    mock_msg.from_user.id = 123
    mock_msg.from_user.username = "test_user"
    mock_msg.answer = AsyncMock()
    mock_msg.reply = AsyncMock()
    return mock_msg

# Фикстура для мока CallbackQuery
@pytest.fixture
def mock_callback(mock_message):
    """Создает мок объекта CallbackQuery с прикрепленным моком Message"""
    callback = AsyncMock(spec=CallbackQuery)
    callback.message = mock_message
    return callback

@pytest.fixture
def mock_router():
    """Mock роутер"""
    router = Router()
    return router
