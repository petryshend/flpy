import json

class Credentials:

    def __init__(self):
        pass

    @staticmethod
    def get():
        with open('credentials.json') as data_file:
            return json.load(data_file)

    @staticmethod
    def save(credentials):
        with open('credentials.json', 'w') as data_file:
            json.dump(credentials, data_file)
            data_file.close()