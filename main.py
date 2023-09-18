import json
import yagmail

import requests
from config import url, rules, SMS_API, SMS_SENDER_NUMBER
from kavenegar import KavenegarAPI


def get_response():
    response = None
    try:
        response = requests.get(url)
    except Exception as e:
        print(f"Error getting response: \t\n {e}")
        input("""
        !!!CONNECTION ERROR
        ***Please check your connection and press enter to retry.
        """)
        get_response()
    if response is not None:
        if response.status_code == 200:
            dats = json.loads(response.text)
            if dats.get('success'):
                print("Data Received!")
                return dats
        print("No data cath!")
    return None


def archive_data(data):
    file_name = f"{data['date']}_{data['timestamp']}"
    with open(f'archive/{file_name}.json', 'w') as f:
        json.dump(data['rates'], f)
    print("Rates archived.")


def send_email(data):
    subject = f"{data['date']}_{data['timestamp']}"
    if rules["mail"]["filter"]:
        body = rate_filter(data["rates"])
    else:
        body = data["rates"]
    recipients = rules["mail"]["recipients"] if "recipients" in\
                                                rules['mail'] else []

    if not recipients:
        recipients = ['abraham.is.sayin@gmail.com']

    try:
        yag = yagmail.SMTP('abraham.is.sayin@gmail.com', 'ejbcktmxstdynkza')
        yag.send(recipients, subject, body)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")


def rate_filter(data):
    print("Filtering rates to desired ones...")
    rates_to_send = {}
    preferred = rules['mail']['preferred'] \
        if 'preferred' in rules['mail'] else []
    for rate in preferred:
        rates_to_send[rate] = data[rate]
    return rates_to_send


def create_msg(data):
    print("checking events to notify... ")
    msg = ''
    preferred = rules['notification']['selected']

    for rate in preferred.keys():
        if data['rates'][rate] <= preferred[rate]['min']:
            msg += f"{data['rates']} reached Minimum\n"

        if data['rates'][rate] <= preferred[rate]['max']:
            msg += f"{data['rates']} reached Maximum\n*\n"
    return msg


def send_notification(msg):
    api = KavenegarAPI(SMS_API)
    params = {'sender': SMS_SENDER_NUMBER,
              'receptor': rules['notification']['receiver'],
              'message': msg
              }
    response = api.sms_send(params)
    print(response)


if __name__ == '__main__':
    data = get_response()
    if data:
        if rules["archive"]:
            archive_data(data)
        if rules['mail']['enable']:
            send_email(data)
        if rules['notification']['enable']:
            msg = create_msg(data)
            print(msg)
            if msg:
                print("HEY something happened! Sending sms...")
                send_notification(msg)
                print('Sent, gl.')
