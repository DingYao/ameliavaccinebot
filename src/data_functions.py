import sys
sys.path.insert(0, 'modules/')

import json
import network_functions
import pandas
import settings
import time_functions


def processScan():
    startDate = time_functions.getStartDate()
    df = pandas.read_json(network_functions.getLocations(startDate))
    filteredDf = filterDf(df)
    filteredDict = convertDfToDict(filteredDf)
    responseHead = (f'*location: earliestSlotTime*\nas of '
                    f'_{time_functions.getCurrentLocalTime()}_\n\n'
                    )
    responseBody = ''
    responseTail = (f'\n*book with [/search1 slotId]\n'
                    f'+ [/search2 slotId] @ /reschedule*'
                    )
    for k, v in filteredDict.items():
        if v is not None:
            v = time_functions.localizeTime(v)
            responseBody += f'{k}: _{v}_\n'
    response = responseHead + responseBody + responseTail
    return response


def processSearch(input, daysAfter, searchType):
    searchList = processSearchList(input)
    startDate = time_functions.getStartDate(daysAfter)
    df = pandas.read_json(network_functions.getLocations(startDate))
    searchedDf = searchDf(df, searchList)
    searchedDict = convertDfToDict(searchedDf)
    responseHead = ''
    responseBody = ''
    responseTail = ''
    if searchType == 1:
        responseHead = (f'*1st slotId: time* for _{" ".join(input)}_\nas of '
                        f'_{time_functions.getCurrentLocalTime()}_\n\n'
                        )
        responseTail = '*book with ^ 1st slotId\n+ [/search2 slotId] @ /reschedule*'
    elif searchType == 2:
        responseHead = (f'*2nd slotId: time* for _{" ".join(input)}_\nas of '
                        f'_{time_functions.getCurrentLocalTime()}_\n\n'
                        )
        responseTail = '*book with [/search1 slotId]\n+ ^ 2nd slotId @ /reschedule*'
    for k, v in searchedDict.items():
        searchedAppointments = json.loads(network_functions.getAppointments(v, startDate))
        responseBody += f'*{k}*\n{processAppointmentsDict(searchedAppointments, searchType)}\n\n'
    response = responseHead + responseBody + responseTail
    return response


def processStatus(uin, bookingCode):
    serverResponse = network_functions.getStatus(uin, bookingCode)
    responseDict = json.loads(serverResponse.text)
    if serverResponse.status_code != 200:
        return f'STATUS ERROR: {responseDict["message"]}'
    responseHead = (f'*{responseDict["name"]}* appointments\n'
                    f'as of _{time_functions.getCurrentLocalTime()}_\n\n'
                    )
    responseTail = (f'*check @ {settings.SUMMARY_PAGE_URL}?uin={uin}&code={bookingCode}&admin=true*')
    response = responseHead + processResponseDict(responseDict) + responseTail
    return response


def processReschedule(uin, bookingCode, firstSlotId, secondSlotId):
    serverResponse = network_functions.rescheduleAppointments(uin, bookingCode, firstSlotId, secondSlotId)
    responseDict = json.loads(serverResponse.text)
    if serverResponse.status_code != 200:
        return f'RESCHEDULE ERROR: {responseDict["message"]}'
    responseHead = (f'*{responseDict["name"]}* appointments _rescheduled_\n'
                    f'as of _{time_functions.getCurrentLocalTime()}_\n\n'
                    )
    responseTail = (f'*check received MOH confirmation SMS\n'
                    f'check @ {settings.SUMMARY_PAGE_URL}?uin={uin}&code={bookingCode}&admin=true*'
                    )
    response = responseHead + processResponseDict(responseDict) + responseTail
    return response


def processSearchList(searchList):
    returnList = []
    for item in searchList:
        returnList.append(item[:1].upper() + item[1:].lower())
    return returnList


def processAppointmentsDict(appointmentsDict, searchType):
    returnText = ''
    appointmentList = []
    for k, v in appointmentsDict.items():
        appointmentList += v
    if len(appointmentList) > 0:
        if searchType == 1:
            for i in range(settings.SLOTS_TO_SHOW_SEARCH1):
                if i == len(appointmentList):
                    break
                returnText += f'{appointmentList[i]["id"]}: _{time_functions.localizeTime(appointmentList[i]["time"])}_\n'
        elif searchType == 2:
            for i in range(settings.SLOTS_TO_SHOW_SEARCH2):
                if i == len(appointmentList):
                    break
                returnText += f'{appointmentList[i]["id"]}: _{time_functions.localizeTime(appointmentList[i]["time"])}_\n'
    else:
        returnText += 'None\n'
    return returnText[:-1]


def processResponseDict(responseDict):
    returnText = ''
    for appointment in responseDict['appointments']:
        appointmentStatus = appointment["status"]
        if appointment["status"] == '':
            appointmentStatus += 'not completed'
        returnText += (f'*{appointment["location"]["name"]}*\n'
                       f'bookingId: _{appointment["id"]}_\n'
                       f'slotId: _{appointment["slot_id"]}_\n'
                       f'address:\n_{appointment["location"]["address"]}_\n'
                       f'time: _{appointment["time"]}_\n'
                       f'status: _{appointmentStatus}_\n\n'
                       )
    return returnText


def filterDf(df):
    return df.loc[df['vaccineType'] == settings.VACCINE_TYPE][['name', 'earliestSlot']].set_index('name')['earliestSlot']


def searchDf(df, searchList):
    df = df[df['name'].str.contains('|'.join(searchList))]
    return df[df['vaccineType'] == settings.VACCINE_TYPE][['name', 'hci_code']].set_index('name')['hci_code']


def convertDfToDict(df):
    return df.to_dict()