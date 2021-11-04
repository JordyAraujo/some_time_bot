import logging
import os
import sys
from config import settings
from telegram import Update, ForceReply, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import locale

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    """Envia uma mensagem quando o Bot é iniciado (comando /start no Telegram)."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Olá {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def main() -> None:
    """Inicia o bot."""
    # Cria o "Updater" com o token do Bot.
    updater = Updater(settings.TOKEN)

    # Seta o "dispatcher" para registrar os manipuladores
    dispatcher = updater.dispatcher

    # Seta o comando /start para chamar sua respectiva função
    dispatcher.add_handler(CommandHandler("start", start))

    # Inicia o Bot de fato
    updater.start_polling()

    # Mantém o Bot rodando até que receba um comando para encerrar a execução
    updater.idle()


if __name__ == '__main__':
    main()
