import os


APPOINTMENTS_ENDPOINT = 'https://appointment.vaccine.gov.sg/api/v1/availability/'
BOT_NAME = 'AmeliaVaccineBot'
DATE_OF_BIRTH = '13-Oct-1994'
END_SEARCH_DATE = '2021-09-30'
HELP_TEXT = (f'*Instructions*\n\n'
             f'1. /scan to find locations with an available 1st appointment\n'
             f'2. /search1 a location to get _slotId_ of the available 1st appointment\n'
             f'3. /search2 the same location to get _slotId_ of an available 2nd appointment 6 weeks later\n'
             f'4. /reschedule [[NRIC/UIN]] [[bookingCode]] [[/search1 slotId]]\n'
             f'[[/search2 slotId]] to reschedule your appointments\n'
             f'5. /status to show your scheduled appointments'
             )
LOCAL_TIMEZONE = 'Asia/Shanghai'
LOCATIONS_ENDPOINT = 'https://appointment.vaccine.gov.sg/api/v1/locations/'
PATIENT_GROUP_ID = 1
SLOTS_TO_SHOW = 10
START_TEXT = (f'Welcome to *{BOT_NAME}*!\n'
              f'_You must have a valid [NRIC/UIN] and [bookingCode] to use /status\n'
              f'and /reschedule_\n\n'
              f'Available Commands:\n'
              f'/start: List Available Commands\n'
              f'/help: Display Instructions\n'
              f'/scan: Scan Earliest 1st Appointment\n'
              f'/search1: Search 1st Appointment at Location(s)\n'
              f'/search2: Search 2nd Appointment at Location(s)\n'
              f'/status: Show Scheduled Appointments\n'
              f'/reschedule: Reschedule Appointments'
              )
STATUS_RESCHEDULE_ENDPOINT = 'https://appointment.vaccine.gov.sg/api/v1/appointments/'
SUMMARY_PAGE_URL = 'https://appointment.vaccine.gov.sg/'
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
VACCINE_TYPE = 'Pfizer'