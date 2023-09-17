import json
import yagmail

import requests
from config import url, rules


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
    if rules["filter"]:
        body = rate_filter(data['rates'])
    else:
        body = data['rates']
    recipients = rules['recipients'] if 'recipients' in rules else []

    if not recipients:
        recipients = ['toofanmohammadi1234@gmail.com']

    try:
        yag = yagmail.SMTP('abraham.is.sayin@gmail.com', 'ejbcktmxstdynkza')
        yag.send(recipients, subject, body)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")


def rate_filter(data):
    rates_to_send = {}
    preferred = rules['preferred'] if 'preferred' in rules else []
    for rate in preferred:
        rates_to_send[rate] = data[rate]
    print("Filter Applied!")
    return rates_to_send


if __name__ == '__main__':
    data = get_response()
    if data:
        archive_data(data)
        if rules['mail']:
            send_email(data)
