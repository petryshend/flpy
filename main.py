from gui import Gui
from mailer import Mailer


def main():
    gui = Gui()
    gui.start()
    
    mailer = Mailer()
    print 'Start Mailer'
    mailer.start()
    print 'Finished Successfully'

if __name__ == '__main__':
    main()