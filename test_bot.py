import pytest
from pyrogram import Client
from pyrogram.types import Message
from main import start, help_command, info_command

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
    assert "Bienvenue! Sélectionnez une action pour commencer" in response.text

def test_help_command(client, message):
    message.text = "/help"
    response = help_command(client, message)
    assert "/start - Démarrer le bot" in response.text
    assert "/help - Afficher cette aide" in response.text

def test_info_command(client, message):
    message.text = "/info"
    response = info_command(client, message)
    assert "Nom : TestUser" in response.text
    assert "ID Utilisateur : 1" in response.text

