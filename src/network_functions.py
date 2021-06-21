import sys
sys.path.insert(0, 'modules/')

import datetime
import requests
import settings


def getLocations():
    data = {
        'startDate': datetime.date.today(),
        'endDate': settings.END_SEARCH_DATE,
        'dob': settings.DATE_OF_BIRTH,
        'patientGroupId': settings.PATIENT_GROUP_ID
    }
    response = requests.get(settings.LOCATIONS_ENDPOINT, params = data,
                                headers = {'content-type': 'application/json'})
    return response.text


def getAppointments(hci_code, daysAfter):
    data = {
        'startDate': datetime.date.today() + datetime.timedelta(days = daysAfter),
        'endDate': settings.END_SEARCH_DATE,
        'isFirstAppt': False,
    }
    response = requests.get(settings.APPOINTMENTS_ENDPOINT + hci_code, params = data,
                                headers = {'content-type': 'application/json'})
    return response.text


def getStatus(uin, bookingCode):
    response = requests.get(f'{settings.STATUS_RESCHEDULE_ENDPOINT}{uin}/{bookingCode}')
    return response


def rescheduleAppointments(uin, bookingCode, firstSlotId, secondSlotId):
    data = f'{{"slot_ids": [{firstSlotId}, {secondSlotId}]}}'
    response = requests.put(f'{settings.STATUS_RESCHEDULE_ENDPOINT}{uin}/{bookingCode}/reschedule', data = data,
                                headers = {'content-type': 'application/json'})
    return response