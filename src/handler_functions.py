import sys
sys.path.insert(0, 'modules/')

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import check_functions
import data_functions
import settings


def start(update, context):
    logging.info('Received /start command')
    update.message.reply_text(settings.START_TEXT, parse_mode = 'Markdown')


def help(update, context):
    logging.info('Received /help command')
    update.message.reply_text(settings.HELP_TEXT, parse_mode = 'Markdown')


def scan(update, context):
    logging.info('Received /scan command')
    
    response = data_functions.processScan()
    update.message.reply_text(response, parse_mode = 'Markdown')


def search1(update, context):
    input = update.message.text.split(" ")[1:]
    inputLog = " ".join(input)
    logging.info(f'Received /search1 command: {inputLog}')
    if inputLog == '':
        update.message.reply_text(
            text='SYNTAX ERROR: Use /search1 [[Location(1) Location(2)...]]', parse_mode='Markdown')
        return
    response = data_functions.processSearch(input, 0, 1)
    update.message.reply_text(response, parse_mode = 'Markdown')


def search2(update, context):
    input = update.message.text.split(" ")[1:]
    inputLog = " ".join(input)
    logging.info(f'Received /search2 command: {inputLog}')
    if inputLog == '':
        update.message.reply_text(
            text='SYNTAX ERROR: Use /search2 [[Location(1) Location(2)...]]', parse_mode='Markdown')
        return
    
    response = data_functions.processSearch(input, 42, 2)
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
    response = data_functions.processStatus(uin, bookingCode)
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
    response = data_functions.processReschedule(uin, bookingCode, firstSlotId, secondSlotId)
    update.message.reply_text(response, parse_mode = 'Markdown')


def get_input(update, context):
    logging.info(f'Received input: {update.message.text}')