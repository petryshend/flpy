import json


class WomenDone:

    filename = 'women.json'

    def __init__(self):
        with open(self.filename) as data_file:
            self.women_done = json.load(data_file)

    def add(self, url, name):
        self.women_done[url] = name
        self.write()

    def get(self):
        return self.women_done

    def remove(self, url):
        if url in self.women_done.keys():
            self.women_done.pop(url, None)
            self.write()

    def clear(self):
        self.women_done = {}
        self.write()

    def write(self):
        with open(self.filename, 'w') as outfile:
            json.dump(self.women_done, outfile)