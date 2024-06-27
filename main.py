import os
import signal
from time import sleep
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_NAME = "bot_session"

# Configuration du logger
logger.add("bot.log", level="DEBUG")

# Initialisation du client Pyrogram avec jeton API
app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Affichage des informations de démarrage
def display_startup_info(api_id, api_hash):
    logger.info("Userbot - Informations de Démarrage")
    logger.info(f"API ID : {api_id}")
    logger.info(f"API Hash : {api_hash}")

display_startup_info(API_ID, API_HASH)

# Handler pour la commande /start
@app.on_message(filters.command("start"))
def start(client, message):
    logger.debug(f"Commande /start reçue de {message.from_user.first_name} dans le chat {message.chat.id}")

    # Création de la présentation avec des boutons
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Action 1", callback_data="action1")],
        [InlineKeyboardButton("Action 2", callback_data="action2")],
        [InlineKeyboardButton("Action 3", callback_data="action3")]
    ])

    message.reply(
        "Bienvenue! Sélectionnez une action pour commencer :",
        reply_markup=keyboard
    )
    logger.info(f"Réponse envoyée pour la commande /start reçue de {message.from_user.first_name}")

# Handler pour les boutons
@app.on_callback_query()
def handle_callback_query(client, callback_query):
    data = callback_query.data
    if data == "action1":
        callback_query.message.edit_text("Vous avez sélectionné Action 1")
        logger.info("Action 1 sélectionnée")
    elif data == "action2":
        callback_query.message.edit_text("Vous avez sélectionné Action 2")
        logger.info("Action 2 sélectionnée")
    elif data == "action3":
        callback_query.message.edit_text("Vous avez sélectionné Action 3")
        logger.info("Action 3 sélectionnée")
    else:
        callback_query.message.edit_text("Action inconnue")

# Ajouter une commande /help
@app.on_message(filters.command("help"))
def help_command(client, message):
    help_text = (
        "/start - Démarrer le bot\n"
        "/help - Afficher cette aide\n"
        "/info - Obtenir des informations sur l'utilisateur\n"
    )
    message.reply(help_text)
    logger.info(f"Réponse envoyée pour la commande /help reçue de {message.from_user.first_name}")

# Ajouter une commande /info pour obtenir des informations sur l'utilisateur
@app.on_message(filters.command("info"))
def info_command(client, message):
    user_info = (
        f"Nom : {message.from_user.first_name}\n"
        f"ID Utilisateur : {message.from_user.id}\n"
    )
    message.reply(user_info)
    logger.info(f"Réponse envoyée pour la commande /info reçue de {message.from_user.first_name}")

# Handler pour tous les messages (pour débogage)
@app.on_message(filters.all)
def log_all_messages(client, message):
    logger.debug(f"Message reçu dans le chat {message.chat.id} de {message.from_user.id} : {message.text}")

def stop_client(signal, frame):
    logger.info("Arrêt du bot...")
    app.stop()
    exit(0)

signal.signal(signal.SIGINT, stop_client)
signal.signal(signal.SIGTERM, stop_client)

# Lancement du bot
try:
    logger.info("Lancement du bot...")
    app.start()

    if app.is_connected:
        logger.info("Bot démarré et connecté avec succès.")
    else:
        logger.error("Échec de la connexion du bot.")

    logger.info("Bot démarré et en attente des messages...")

    while True:
        sleep(1)
except Exception as e:
    logger.error(f"Erreur lors de l'exécution du bot : {e}")
    app.stop()

