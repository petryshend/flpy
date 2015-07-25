from Tkconstants import TOP
from Tkinter import Tk, Entry, Label, mainloop, Button, StringVar, Frame
from credentials import Credentials


class Gui:

    def __init__(self):
        self.root = Tk()
        self.credentials_frame = Frame(self.root)
        self.credentials_frame.pack(side=TOP)
        self.username_entry_variable = StringVar()
        self.username_entry_variable.set(Credentials.get()['username'])
        self.password_entry_variable = StringVar()
        self.password_entry_variable.set(Credentials.get()['password'])
        self.username_entry = Entry(self.credentials_frame, textvariable=self.username_entry_variable)
        self.password_entry = Entry(self.credentials_frame, textvariable=self.password_entry_variable)

    def start(self):
        self.construct_credentials_fields()
        mainloop()

    def construct_credentials_fields(self):
        username_label = Label(self.credentials_frame, text='Username')
        password_label = Label(self.credentials_frame, text='Password')
        username_label.grid(row=0, column=0)
        password_label.grid(row=1, column=0)

        save_button = Button(self.credentials_frame, text='Save', command=self.save_credentials)
        start_mailer_button = Button(self.credentials_frame, text='Start mailer', command=self.close_gui)

        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)
        save_button.grid(row=2, column=0)
        start_mailer_button.grid(row=2, column=1)

    def save_credentials(self):
        credentials = {
            'username': self.username_entry_variable.get(),
            'password': self.password_entry_variable.get()
        }
        Credentials.save(credentials)

    def close_gui(self):
        self.root.quit()


if __name__ == '__main__':
    gui = Gui()
    gui.start()