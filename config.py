
# fixer.io
BASE_PATH = 'http://data.fixer.io/api/latest?access_key='
FIXER_API_KEY = '6c2872319dad58012fe8e4057a8d7051'

url = BASE_PATH + FIXER_API_KEY


# sms sender api (Default kavenegar.com)
SMS_API = '5A7A774442364B45485A68656457304B6A313648' \
        '326C67344969695458445A765654504A2F356E4C2B74413D'
SMS_SENDER_NUMBER = '1000689696'


# Local Rules
rules = {
    "archive": True,
    "mail": {
        "enable": True,
        "filter": True,
        "preferred": ["BTC", "USD", "CAD"],
        "recipients": [
            # 'toofanmohammadi1234@gmail.com',
            # 'toofanmohammadi4321@gmail.com'
        ]
    },
    "notification": {
        "enable": True,
        "receiver": '',
        "selected": {
            "BSD": {"min": 100, "max": 1},
            "CAD": {"min": 100, "max": 100}
        }
    }
}
