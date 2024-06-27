import pytest
from pyrogram import Client
from pyrogram.types import Message
from main import start

@pytest.fixture
def client():
    return Client("test_session", api_id=20674474, api_hash="ad16c17657dec1f64e290f35fa44dcf4", bot_token="7209901875:AAFwf7i3NQEuTAdqaVJGXYkBQwI1xDn26lw")

@pytest.fixture
def message():
    return Message(
        id=1,
        chat={"id": 1, "type": "private"},
        from_user={"id": 1, "is_bot": False, "first_name": "TestUser"},
        text="/start"
    )

def test_start_command(client, message):
    response = start(client, message)
    assert "Bienvenue! Le bot est actif." in response.text

