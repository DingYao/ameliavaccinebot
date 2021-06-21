import sys
sys.path.insert(0, 'modules/')

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import check_functions
import data_functions
import network_functions
import pandas as pd
import settings
import time_functions


def start(update, context):
    logging.info('Received /start command')
    update.message.reply_text(settings.START_TEXT, parse_mode = 'Markdown')


def help(update, context):
    logging.info('Received /help command')
    update.message.reply_text(settings.HELP_TEXT, parse_mode = 'Markdown')


def scan(update, context):
    logging.info('Received /scan command')
    df = pd.read_json(network_functions.getLocations())
    filteredDf = data_functions.filterDf(df)
    filteredDict = data_functions.convertDfToDict(filteredDf)
    response = (f'*location: earliestSlotTime*\nas of '
                f'_{time_functions.getCurrentLocalTime()}_\n\n'
                )
    for k, v in filteredDict.items():
        if v is not None:
            v = time_functions.localizeTime(v)
            response += f'{k}: _{v}_\n'
    response = response[:-1] + (f'\n\n*book with [/search1 slotId]\n'
                                f'+ [/search2 slotId] @ /reschedule*'
                                )
    update.message.reply_text(response, parse_mode = 'Markdown')


def search1(update, context):
    input = update.message.text.split(" ")[1:]
    inputLog = " ".join(input)
    logging.info(f'Received /search1 command: {inputLog}')
    if inputLog == '':
        update.message.reply_text(
            text='SYNTAX ERROR: Use /search1 [[Location(1) Location(2)...]]', parse_mode='Markdown')
        return
    responseHead = (f'*1st slotId: time* for _{inputLog}_\nas of '
                    f'_{time_functions.getCurrentLocalTime()}_\n\n'
                    )
    responseTail = '*book with ^ 1st slotId\n+ [/search2 slotId] @ /reschedule*'
    response = responseHead + data_functions.processSearch(input, 0) + responseTail
    update.message.reply_text(response, parse_mode = 'Markdown')


def search2(update, context):
    input = update.message.text.split(" ")[1:]
    inputLog = " ".join(input)
    logging.info(f'Received /search2 command: {inputLog}')
    if inputLog == '':
        update.message.reply_text(
            text='SYNTAX ERROR: Use /search2 [[Location(1) Location(2)...]]', parse_mode='Markdown')
        return
    responseHead = (f'*2nd slotId: time* for _{inputLog}_\nas of '
                    f'_{time_functions.getCurrentLocalTime()}_\n\n'
                    )
    responseTail = '*book with [/search1 slotId]\n+ ^ 2nd slotId @ /reschedule*'
    response = responseHead + data_functions.processSearch(input, 42) + responseTail
    update.message.reply_text(response, parse_mode = 'Markdown')


def status(update, context):
    input = update.message.text.split(" ")[1:]
    inputLog = " ".join(input)
    logging.info(f'Received /status command: {inputLog}')
    if len(input) != 2:
        update.message.reply_text(
            text = (f'SYNTAX ERROR: Use /status\n'
                    f'[[NRIC/UIN]] [[bookingCode]]'
                    ), parse_mode='Markdown')
        return
    uin = input[0].upper()
    bookingCode = input[1].upper()
    if not check_functions.checkNric(uin):
        update.message.reply_text(
            text='VALIDATION ERROR: Please enter a valid [[NRIC/UIN]]', parse_mode='Markdown')
        return
    if len(bookingCode) != 10:
        update.message.reply_text(
            text='VALIDATION ERROR: Please enter a valid [[bookingCode]]', parse_mode='Markdown')
        return
    serverResponse = network_functions.getStatus(uin, bookingCode)
    response = data_functions.processStatusResponse(serverResponse)
    if 'ERROR:' not in response:
        response += (f'*check @ {settings.SUMMARY_PAGE_URL}?uin={uin}&code={bookingCode}&admin=true*'
        )
    update.message.reply_text(response, parse_mode = 'Markdown')


def reschedule(update, context):
    input = update.message.text.split(" ")[1:]
    inputLog = " ".join(input)
    logging.info(f'Received /reschedule command: {inputLog}')
    if len(input) != 4:
        update.message.reply_text(
            text=(f'SYNTAX ERROR: Use /reschedule [[NRIC/UIN]] [[bookingCode]]\n'
                  f'[[/search1 slotId]] [[/search2 slotId]]'
                  ), parse_mode='Markdown')
        return
    uin = input[0].upper()
    bookingCode = input[1].upper()
    firstSlotId = input[2]
    secondSlotId = input[3]
    if not check_functions.checkNric(uin):
        update.message.reply_text(
            text='VALIDATION ERROR: Please enter a valid [[NRIC/UIN]]', parse_mode='Markdown')
        return
    if len(bookingCode) != 10:
        update.message.reply_text(
            text='VALIDATION ERROR: Please enter a valid [[bookingCode]]', parse_mode='Markdown')
        return
    if len(firstSlotId) != 6:
        update.message.reply_text(
            text='VALIDATION ERROR: Please enter a valid [[/search1 slotId]]', parse_mode='Markdown')
        return
    if len(secondSlotId) != 6:
        update.message.reply_text(
            text='VALIDATION ERROR: Please enter a valid [[/search2 slotId]]', parse_mode='Markdown')
        return
    serverResponse = network_functions.rescheduleAppointments(uin, bookingCode, firstSlotId, secondSlotId)
    response = data_functions.processRescheduleResponse(serverResponse)
    if 'ERROR:' not in response:
        response += (f'*check received MOH confirmation SMS\n'
                     f'check @ {settings.SUMMARY_PAGE_URL}?uin={uin}&code={bookingCode}&admin=true*'
                     )
    update.message.reply_text(response, parse_mode = 'Markdown')


def get_input(update, context):
    logging.info(f'Received input: {update.message.text}')