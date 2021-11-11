import calendar

import pendulum
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import messages
import utils


def create_callback_data(action,year,month,day):
    return messages.CALENDAR_CALLBACK + ";" + ";".join([action,str(year),str(month),str(day)])


def create_calendar(year=None,month=None):
    now = pendulum.now('America/Fortaleza')
    if year == None: year = now.year
    if month == None: month = now.month
    data_ignore = create_callback_data("IGNORE", year, month, 0)
    keyboard = []
    #First row - Month and Year
    row=[]
    row.append(InlineKeyboardButton("<",callback_data=create_callback_data("PREV-YEAR",year,month,0)))
    row.append(InlineKeyboardButton(str(year),callback_data=data_ignore))
    row.append(InlineKeyboardButton(">",callback_data=create_callback_data("NEXT-YEAR",year,month,0)))
    keyboard.append(row)
    row=[]
    row.append(InlineKeyboardButton("<",callback_data=create_callback_data("PREV-MONTH",year,month,0)))
    row.append(InlineKeyboardButton(calendar.month_name[month],callback_data=data_ignore))
    row.append(InlineKeyboardButton(">",callback_data=create_callback_data("NEXT-MONTH",year,month,0)))
    keyboard.append(row)
    #Second row - Week Days
    row=[]
    for day in ["Seg","Ter","Qua","Qui","Sex","Sáb","Dom"]:
        row.append(InlineKeyboardButton(day,callback_data=data_ignore))
    keyboard.append(row)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row=[]
        for day in week:
            if(day==0):
                row.append(InlineKeyboardButton(" ",callback_data=data_ignore))
            else:
                row.append(InlineKeyboardButton(str(day),callback_data=create_callback_data("DAY",year,month,day)))
        keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def process_calendar_selection(update,context):
    ret_data = (False,None)
    query = update.callback_query
    (_,action,year,month,day) = utils.separate_callback_data(query.data)
    curr = pendulum.datetime(int(year), int(month), 1, tz='America/Fortaleza')
    match action:
        case 'IGNORE':
            context.bot.answer_callback_query(callback_query_id= query.id)
        case 'DAY':
            context.bot.edit_message_text(text=query.message.text,
                chat_id=query.message.chat_id,
                message_id=query.message.message_id
                )
            ret_data = True,pendulum.datetime(int(year), int(month), int(day), tz='America/Fortaleza')
        case 'PREV-MONTH':
            prem = curr.subtract(months=1)
            context.bot.edit_message_text(text=query.message.text,
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                reply_markup=create_calendar(int(prem.year),int(prem.month)))
        case 'NEXT-MONTH':
            nem = curr.add(months=1)
            context.bot.edit_message_text(text=query.message.text,
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                reply_markup=create_calendar(int(nem.year),int(nem.month)))
        case 'PREV-YEAR':
            prey = curr.subtract(years=1)
            context.bot.edit_message_text(text=query.message.text,
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                reply_markup=create_calendar(int(prey.year),int(prey.month)))
        case 'NEXT-YEAR':
            ney = curr.add(years=1)
            context.bot.edit_message_text(text=query.message.text,
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                reply_markup=create_calendar(int(ney.year),int(ney.month)))
        case _:
            context.bot.answer_callback_query(callback_query_id= query.id,text="Something went wrong!")
    return ret_data