import sys
sys.path.insert(0, 'modules/')

import datetime
import pytz
import settings


def getCurrentLocalTime():
    return datetime.datetime.now(pytz.timezone(settings.LOCAL_TIMEZONE)).replace(microsecond = 0)


def localizeTime(v):
    try:
        v = datetime.datetime.strptime(v[:-5], "%Y-%m-%dT%H:%M:%S")
    except:
        pass
    v = pytz.utc.localize(v).astimezone(pytz.timezone(settings.LOCAL_TIMEZONE))
    return v