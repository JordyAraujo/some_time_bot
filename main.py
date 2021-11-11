import logging

import peewee
from telegram.ext import CallbackQueryHandler, CommandHandler, Updater

from commands import inline_handler, set_scheduled_date, start
from config import settings
from Models.Event import Event
from Models.Group import Group

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def main() -> None:
    """Inicia o bot."""
    # Cria o "Updater" com o token do Bot.
    updater = Updater(settings.TOKEN)

    # Seta o "dispatcher" para registrar os manipuladores
    dispatcher = updater.dispatcher

    # Seta o comando /start para chamar sua respectiva função
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("waitFor",set_scheduled_date))
    dispatcher.add_handler(CallbackQueryHandler(inline_handler))

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
