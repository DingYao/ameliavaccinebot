# AmeliaVaccineBot

Telegram bot to scan, search, reschedule, and track Singapore Covid-19 vaccination appointments

- [AmeliaVaccineBot on Telegram](https://t.me/AmeliaVaccineBot)

## Example commands

1. `/scan` to find locations with an available 1st appointment
2. `/search1 [a location]` to get _slotId_ of the available 1st appointment
3. `/search2 [the same location]` to get _slotId_ of an available 2nd appointment 6 weeks later
4. `/reschedule [NRIC/UIN] [bookingCode] [/search1 slotId] [/search2 slotId]` to reschedule your appointments
5. `/status [NRIC/UIN] [bookingCode]` to show your scheduled appointments

## Getting started

### Setup Python environment

```bash
pip3 install -r requirements.txt -t modules/
sudo timedatectl set-timezone Asia/Shanghai
```

### Configure AmeliaVaccineBot

Configure these settings in the _src/settings.py_ file

- `BOT_NAME`: Bot name
- `DATE_OF_BIRTH`: Date of birth
- `END_SEARCH_DATE`: End search date
- `SLOTS_TO_SHOW_SEARCH1`: Slots to show per location for /search1
- `SLOTS_TO_SHOW_SEARCH2`: Slots to show per location for /search2
- `PATIENT_GROUP_ID`: Patient group id
- `VACCINE_TYPE`: Vaccine type

### Run AmeliaVaccineBot

```bash
export TELEGRAM_BOT_TOKEN=[TELEGRAM_BOT_TOKEN]
python3 src
```
