import pytest
from main import main
from fixtures import mock_bot, mock_dispatcher, mock_set_my_commands, mock_router, mock_set_up_logger

@pytest.mark.asyncio
async def test_main(mock_bot, mock_dispatcher, mock_router, mock_set_my_commands, mock_set_up_logger):
    # Вызов функции main
    await main()

    # Проверка
    mock_dispatcher.start_polling.assert_awaited_once_with(mock_bot)

    # TODO -техдолг: доделать вызовы функции
    # mock_dispatcher.include_routers.assert_awaited_once_with(mock_router)
    # mock_set_my_commands.assert_awaited_once_with(mock_bot)
    # mock_set_up_logger.assert_awaited_once()