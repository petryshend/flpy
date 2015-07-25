import json


class WomenDone:

    filename = 'women.json'

    def __init__(self):
        with open(self.filename) as data_file:
            self.women_done = json.load(data_file)

    def add(self, url):
        self.women_done['urls'].append(url)
        self.write()

    def get(self):
        return self.women_done['urls']

    def remove(self, url):
        if url in self.women_done['urls']:
            self.women_done['urls'].remove(url)
            self.write()

    def clear(self):
        self.women_done['urls'] = []
        self.write()

    def write(self):
        with open(self.filename, 'w') as outfile:
            json.dump(self.women_done, outfile)