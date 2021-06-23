from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import settings
import handler_functions
import logging
import sys
sys.path.insert(0, 'modules/')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


updater = Updater(token=settings.TELEGRAM_BOT_TOKEN)
dispatcher = updater.dispatcher
job = updater.job_queue
logging.info('Bot initialized')

# Add CommandHandler to Dispatcher
start_handler = CommandHandler('start', handler_functions.start)
help_handler = CommandHandler('help', handler_functions.help)
scan_handler = CommandHandler('scan', handler_functions.scan)
search1_handler = CommandHandler('search1', handler_functions.search1)
search2_handler = CommandHandler('search2', handler_functions.search2)
status_handler = CommandHandler('status', handler_functions.status)
reschedule_handler = CommandHandler('reschedule', handler_functions.reschedule)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(scan_handler)
dispatcher.add_handler(search1_handler)
dispatcher.add_handler(search2_handler)
dispatcher.add_handler(status_handler)
dispatcher.add_handler(reschedule_handler)

# Add MessageHandler to Dispatcher
input_handler = MessageHandler(Filters.text, handler_functions.get_input)
dispatcher.add_handler(input_handler)

# Start Bot
updater.start_polling()

# Run Bot until Terminated
updater.idle()
