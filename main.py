import locale
import logging
import os
import sys

from Models.Group import Group
from Models.Event import Event
import peewee

from telegram import ForceReply, ParseMode, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from config import settings

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Olá {user.mention_markdown_v2()}\!'
    )


def teste(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(str(update.message.chat_id) + ": " + update.message.text)



def main() -> None:
    """Inicia o bot."""
    # Cria o "Updater" com o token do Bot.
    updater = Updater(settings.TOKEN)

    # Seta o "dispatcher" para registrar os manipuladores
    dispatcher = updater.dispatcher

    # Seta o comando /start para chamar sua respectiva função
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("teste", teste))

    # Inicia o Bot de fato
    updater.start_polling()

    # Mantém o Bot rodando até que receba um comando para encerrar a execução
    updater.idle()


if __name__ == '__main__':
    try:
        Group.create_table()
        print("Groups table created succesfully")
    except peewee.OperationalError:
        print("Groups table already exists")


    try:
        Event.create_table()
        print("Events table created succesfully")
    except peewee.OperationalError:
        print("Events table already exists")

        
    main()
