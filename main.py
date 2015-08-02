from gui import Gui
from mailer import Mailer

import time


def main():
    gui = Gui()
    gui.start()

    while True:
        try:
            print 'Start Mailer'
            mailer = Mailer()
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