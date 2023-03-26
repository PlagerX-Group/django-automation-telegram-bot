from unittest.mock import patch, MagicMock

import pytest
from django.test import Client
from telegram import Update, User, Message
from telegram.ext import Updater, CallbackContext, Dispatcher


@pytest.fixture(scope="module")
def client() -> Client:
    return Client()


@pytest.fixture(scope='function')
def tgbot_updater_mock() -> Updater:
    with patch('telegram.ext.Updater') as mocked_updater:
        yield mocked_updater


@pytest.fixture(scope="function")
def tgbot_update_and_context_mock() -> tuple[Update, CallbackContext]:
    user = User(id=1, first_name='FirstName', last_name='LastName', username='username', is_bot=False)
    message = Message(message_id=1, text='text', chat=MagicMock(), date=MagicMock(), from_user=user)
    update = Update(update_id=1, message=message)
    dispatcher = Dispatcher(MagicMock(), MagicMock())
    context = CallbackContext(dispatcher=dispatcher)
    return update, context
