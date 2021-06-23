import sys
sys.path.insert(0, 'modules/')

import datetime
import pytz
import settings


def localizeTime(string):
    try:
        string = datetime.datetime.strptime(string[:-5], "%Y-%m-%dT%H:%M:%S")
    except:
        pass
    string = pytz.utc.localize(string).astimezone(pytz.timezone(settings.LOCAL_TIMEZONE))
    return string


def getCurrentLocalTime():
    return datetime.datetime.now(pytz.timezone(settings.LOCAL_TIMEZONE)).replace(microsecond = 0)


def getStartDate(daysAfter = 0):
    return datetime.date.today() + datetime.timedelta(days = daysAfter)