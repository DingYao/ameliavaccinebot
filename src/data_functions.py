import sys
sys.path.insert(0, 'modules/')

import data_functions
import json
import network_functions
import pandas as pd
import settings
import time_functions


def processSearchList(searchList):
    returnList = []
    for item in searchList:
        returnList.append(item[:1].upper() + item[1:].lower())
    return returnList


def processSearch(input, daysAfter):
    searchList = processSearchList(input)
    df = pd.read_json(network_functions.getLocations())
    searchedDf = data_functions.searchDf(df, searchList)
    searchedDict = data_functions.convertDfToDict(searchedDf)
    responseBody = ''
    for k, v in searchedDict.items():
        searchedAppointments = json.loads(network_functions.getAppointments(v, daysAfter))
        responseBody += f'*{k}*\n{processAppointmentsDict(searchedAppointments)}\n\n'
    return responseBody


def processAppointmentsDict(appointmentsDict):
    appointmentList = []
    returnText = ''
    for k, v in appointmentsDict.items():
        appointmentList += v
    if len(appointmentList) > 0:
        for i in range(settings.SLOTS_TO_SHOW):
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


def processStatusResponse(serverResponse):
    returnText = ''
    responseDict = json.loads(serverResponse.text)
    if serverResponse.status_code != 200:
        return f'STATUS ERROR: {responseDict["message"]}'
    returnText += (f'*{responseDict["name"]}* appointments\n'
                   f'as of _{time_functions.getCurrentLocalTime()}_\n\n'
                   )
    returnText += processResponseDict(responseDict)
    return returnText


def processRescheduleResponse(serverResponse):
    returnText = ''
    responseDict = json.loads(serverResponse.text)
    if serverResponse.status_code != 200:
        return f'RESCHEDULE ERROR: {responseDict["message"]}'
    returnText += (f'*{responseDict["name"]}* appointments _rescheduled_\n'
                   f'as of _{time_functions.getCurrentLocalTime()}_\n\n'
                   )
    returnText += processResponseDict(responseDict)
    return returnText


def filterDf(df):
    return df.loc[df['vaccineType'] == settings.VACCINE_TYPE][['name', 'earliestSlot']].set_index('name')['earliestSlot']


def searchDf(df, searchList):
    df = df[df['name'].str.contains('|'.join(searchList))]
    return df[df['vaccineType'] == settings.VACCINE_TYPE][['name', 'hci_code']].set_index('name')['hci_code']


def convertDfToDict(df):
    return df.to_dict()