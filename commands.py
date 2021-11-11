from telegram import ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext

import messages
import telegramcalendar
import utils


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Olá {user.mention_markdown_v2()}\!'
    )


def set_scheduled_date(update, context):
    chat_id = str(update.message.chat_id)
    data = telegramcalendar.create_calendar()
    update.message.reply_text(text=messages.calendar_message, reply_markup=data)


def inline_handler(update, context):
    query = update.callback_query
    (kind, _, _, _, _) = utils.separate_callback_data(query.data)
    if kind == messages.CALENDAR_CALLBACK:
        inline_calendar_handler(update, context)


def inline_calendar_handler(update, context):
    selected,date = telegramcalendar.process_calendar_selection(update, context)
    if selected:
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                        text=messages.calendar_response_message % (date.strftime("%d/%m/%Y")),
                        reply_markup=ReplyKeyboardRemove())
