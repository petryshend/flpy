from mailer import Mailer


def main():
    mailer = Mailer()
    mailer.start()
    print 'Finished Successfully'

if __name__ == '__main__':
    main()