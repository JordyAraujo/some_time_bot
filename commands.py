from telegram import ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext

from Models.Group import Group
from Models.User import User
from Models.Event import Event
import messages
import telegramcalendar
import utils


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Olá {user.mention_markdown_v2()}\!'
    )

def set_scheduled_date(update, context):
    chat_is_group = update.message.chat.type == "group"
    
    if(chat_is_group):
        group_id = str(update.message.chat.id)
        group_name = str(update.message.chat.title)
        group, created = Group.get_or_create(
            group_id = group_id, 
            defaults={
                'group_name': group_name
                }
            )
    else:
        user_id = str(update.message.chat.id)
        user_username = str(update.message.chat.username)
        user, created = User.get_or_create(
            user_id = user_id, 
            defaults={
                'user_username': user_username
                }
            )
    date = telegramcalendar.create_calendar()
    event = Event(
        event_title = context.args[0],
        event_group = group if chat_is_group else None, 
        event_user = None if chat_is_group else user,
        event_due = date
    )
    update.message.reply_text(text=messages.calendar_message, reply_markup=event.event_due)


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
