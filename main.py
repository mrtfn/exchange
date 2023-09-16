import json

import requests
from config import url


def get_response():
    response = requests.get(url)
    if response.status_code == 200:
        dats = json.loads(response.text)
        print(dats)
        if dats.get('success'):
            return dats
    return None


def archive(date, time_stamp, rates):
    file_name = str(date) + '_' + str(time_stamp)
    with open(f'archive/{file_name}.json', 'w') as f:
        json.dump(rates, f)


if __name__ == '__main__':
    data = get_response()
    if data:
        print(data.keys())
        archive(data['date'], data['timestamp'], data['rates'])
