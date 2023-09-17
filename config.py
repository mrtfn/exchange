BASE_PATH = 'http://data.fixer.io/api/latest?access_key='

API_KEY = '6c2872319dad58012fe8e4057a8d7051'


url = BASE_PATH + API_KEY

rules = {
    "archive": True,
    "mail": True,
    "filter": False,
    # if filter=true then preferred list will apply
    "preferred": ["BTC", "USD", "CAD"],
    "recipients": [
        'toofanmohammadi1234@gmail.com',
        'toofanmohammadi4321@gmail.com'
    ]

}
