from gui import Gui
from mailer import Mailer

import time

only_with_photos = 0

def main():
    global only_with_photos
    gui = Gui()
    gui.start()
    only_with_photos = Gui.only_with_photos.get()
    while True:
        try:
            print 'Start Mailer'
            mailer = Mailer(only_with_photos)
            mailer.start()
            print 'Finished Successfully'
        except Exception:
            print 'Something went wrong... Restarting...'
            mailer.close_mailer()
            time.sleep(10)
        else:
            print 'Finished without exceptions'
            break

if __name__ == '__main__':
    main()